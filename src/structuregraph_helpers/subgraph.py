"""Extract subgraphs from structure graphs."""
import warnings
from collections import defaultdict
from typing import List, Tuple

import networkx as nx
import numpy as np
from pymatgen.analysis.graphs import MoleculeGraph, StructureGraph
from pymatgen.core import Element, Molecule, Structure

__all__ = ("get_subgraphs_as_molecules",)


def _is_in_cell(frac_coords: np.ndarray) -> bool:
    return (frac_coords <= 1).all()


def _is_any_atom_in_cell(frac_coords: np.ndarray) -> bool:
    return any(_is_in_cell(row) for row in frac_coords)


def _get_mass(atomic_symbol: str) -> float:
    elem = Element(atomic_symbol)
    return elem.atomic_mass


def com(xyz: np.ndarray, mass: np.ndarray) -> float:
    """Compute the center of mass of a set of atoms."""
    mass = mass.reshape((-1, 1))
    return (xyz * mass).mean(0)


def _select_parts_in_cell(
    molecules: List[Molecule],
    graphs: List[MoleculeGraph],
    indices: List[List[int]],
    indices_here: List[List[int]],
    centers: List[np.ndarray],
    fractional_coordinates: np.ndarray,
    coordinates: np.ndarray,
) -> Tuple[List[Molecule], List[MoleculeGraph], List[List[int]]]:
    valid_indices = defaultdict(list)
    for i, ind in enumerate(indices_here):
        frac_coords = fractional_coordinates[ind]

        if _is_any_atom_in_cell(frac_coords):
            sorted_idx = sorted(indices[i])
            valid_indices[str(sorted_idx)].append(i)

    molecules_ = []
    selected_indices = []
    graphs_ = []
    centers_ = []
    coordinates_ = []

    for _, v in valid_indices.items():
        for index in v:
            selected_indices.append(indices[index])
            molecules_.append(molecules[index])
            graphs_.append(graphs[index])
            centers_.append(centers[index])
            coordinates_.append(coordinates[index])

    return molecules_, graphs_, selected_indices, centers_, coordinates_


def get_subgraphs_as_molecules(  # noqa:C901
    structure_graph: StructureGraph,
    use_weights: bool = False,
    return_unique: bool = True,
    disable_boundary_crossing_check: bool = False,
    filter_in_cell: bool = True,
    prune_long_edges: bool = False,
) -> Tuple[
    List[Molecule], List[MoleculeGraph], List[List[int]], List[np.ndarray], List[np.ndarray]
]:
    """Isolates connected components as molecules from a StructureGraph.

    Copied from http://pymatgen.org/_modules/pymatgen/analysis/graphs.html#StructureGraph.get_subgraphs_as_molecules
    and removed the duplicate check and added pruning of long edges that seem to cause
    issues in some cases.

    This function also returns more info than the original function.

    .. warning::

        This edge pruning is a hack and should be removed when the underlying issue is fixed.

    Args:
        structure_graph (StructureGraph): Structuregraph
        use_weights (bool): If True, use weights for the edge matching
        return_unique (bool): If true, it only returns the unique molecules.
            If False, it will return all molecules that
            are completely included in the unit cell
            and fragments of the ones that are only partly in the cell
        disable_boundary_crossing_check (bool): If true, it will not check
            if the molecules are crossing the boundary of the unit cell.
            Default is False.
        filter_in_cell (bool): If True, it will only return molecules
            that have at least one atom in the cell
        prune_long_edges (bool): If True, it will remove long edges.
            This is somewhat of a hack to workaround a bug i suspect
            in the __mul__ method of StructureGraph.

    Returns:
        Tuple[List[Molecule], List[MoleculeGraph], List[List[int]], List[np.ndarray], List[np.ndarray]]:
            A tuple of (molecules, graphs, indices, centers, coordinates)
    """
    # creating a supercell is an easy way to extract
    # molecules (and not, e.g., layers of a 2D crystal)
    # without adding extra logic

    sg = structure_graph.__copy__()
    sg.structure = Structure.from_sites(sg.structure.sites)

    try:
        node_attributes = nx.get_node_attributes(sg.graph, "idx")
        if len(node_attributes) == 0:
            raise KeyError("No node attributes found")
    except KeyError:
        warnings.warn("No node attributes found. Using indices as node attributes.")
        nx.set_node_attributes(
            sg.graph,
            name="idx",
            values=dict(zip(range(len(structure_graph)), range(len(structure_graph)))),
        )

    # This the __mul__ method seems buggy.
    # potentially this issue here https://github.com/materialsproject/pymatgen/issues/1309
    supercell_sg = sg * (3, 3, 3)
    s_indices = np.arange(len(supercell_sg.structure))
    nx.set_node_attributes(
        supercell_sg.graph, dict(zip(s_indices, supercell_sg.structure.cart_coords)), "coords"
    )

    # make undirected to find connected subgraphs
    supercell_sg.graph = nx.Graph(supercell_sg.graph)

    if prune_long_edges:
        edges_to_remove = []
        for u, v, _ in supercell_sg.graph.edges(data=True):
            # ToDo: make this dependent on the cutoffidct
            if (
                np.linalg.norm(
                    supercell_sg.graph.nodes(data=True)[u]["coords"]
                    - supercell_sg.graph.nodes(data=True)[v]["coords"]
                )
                > 3
            ):
                edges_to_remove.append((u, v))

        for edge_to_remove in edges_to_remove:
            supercell_sg.graph.remove_edge(*edge_to_remove)

    # find subgraphs
    all_subgraphs = [
        supercell_sg.graph.subgraph(c).copy() for c in nx.connected_components(supercell_sg.graph)
    ]

    # discount subgraphs that lie across *supercell* boundaries
    # these will subgraphs representing crystals
    molecule_subgraphs = []

    for subgraph in all_subgraphs:
        if disable_boundary_crossing_check:
            molecule_subgraphs.append(nx.MultiDiGraph(subgraph))
        else:
            intersects_boundary = any(
                (d["to_jimage"] != (0, 0, 0) for u, v, d in subgraph.edges(data=True))
            )
            if not intersects_boundary:
                molecule_subgraphs.append(nx.MultiDiGraph(subgraph))

    # add specie names to graph to be able to test for isomorphism
    for subgraph in molecule_subgraphs:
        for node in subgraph:
            subgraph.add_node(
                node,
                specie=str(supercell_sg.structure[node].specie),
                coord=supercell_sg.structure[node].coords,
            )

    unique_subgraphs = []

    def node_match(n1, n2):
        return n1["specie"] == n2["specie"]

    def edge_match(e1, e2):
        if use_weights:
            return e1["weight"] == e2["weight"]
        return True

    if return_unique:
        for subgraph in molecule_subgraphs:
            already_present = [
                nx.is_isomorphic(subgraph, g, node_match=node_match, edge_match=edge_match)
                for g in unique_subgraphs
            ]

            if not any(already_present):
                unique_subgraphs.append(subgraph)

    def make_mols(molecule_subgraphs=None, center=False):
        if molecule_subgraphs is None:
            molecule_subgraphs = molecule_subgraphs
        molecules = []
        indices = []
        indices_here = []
        mol_centers = []
        coordinates = []
        for subgraph in molecule_subgraphs:
            idx = [subgraph.nodes[n]["idx"] for n in subgraph.nodes()]
            coords = np.array([subgraph.nodes()[i]["coord"] for i in subgraph.nodes()])
            species = [supercell_sg.structure[n].specie for n in subgraph.nodes()]
            idx_here = list(subgraph.nodes())
            molecule = Molecule(species, coords)  # site_properties={"binding": binding}

            masses = np.array(
                [_get_mass(str(supercell_sg.structure[idx].specie)) for idx in idx_here]
            )
            mol_centers.append(com(supercell_sg.structure.cart_coords[idx_here], masses))
            # shift so origin is at center of mass
            if center:
                molecule = molecule.get_centered_molecule()
            indices.append(idx)
            molecules.append(molecule)
            indices_here.append(idx_here)
            coordinates.append(coords)
            assert len(subgraph) == len(coords) == len(idx) == len(idx_here)
        return molecules, indices, indices_here, mol_centers, coordinates

    def relabel_graph(multigraph):
        mapping = dict(zip(multigraph, range(0, len(multigraph.nodes()))))
        return nx.readwrite.json_graph.adjacency_data(nx.relabel_nodes(multigraph, mapping))

    if return_unique:
        mol, idx, indices_here, centers, coordinates = make_mols(unique_subgraphs, center=True)
        return_subgraphs = unique_subgraphs
        return (
            mol,
            [MoleculeGraph(mol, relabel_graph(graph)) for mol, graph in zip(mol, return_subgraphs)],
            idx,
            centers,
            coordinates,
        )

    mol, idx, indices_here, centers, coordinates = make_mols(molecule_subgraphs)

    return_subgraphs = [
        MoleculeGraph(mol, relabel_graph(graph)) for mol, graph in zip(mol, molecule_subgraphs)
    ]

    if filter_in_cell:
        mol, return_subgraphs, idx, centers, coordinates = _select_parts_in_cell(
            mol,
            return_subgraphs,
            idx,
            indices_here,
            centers,
            sg.structure.lattice.get_fractional_coords(supercell_sg.structure.cart_coords),
            coordinates,
        )

    return mol, return_subgraphs, idx, centers, coordinates
