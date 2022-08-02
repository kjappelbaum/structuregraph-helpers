"""Helpers for creating graphs."""
import os
from typing import Iterable, Tuple

import networkx as nx
import yaml
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis.local_env import (
    BrunnerNN_relative,
    CrystalNN,
    CutOffDictNN,
    EconNN,
    MinimumDistanceNN,
    NearNeighbors,
    VoronoiNN,
)
from pymatgen.core import Structure

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(_THIS_DIR, "data", "tuned_vesta.yml"), "r", encoding="utf8") as handle:
    _VESTA_CUTOFFS = yaml.load(handle, Loader=yaml.UnsafeLoader)  # noqa: S506


with open(os.path.join(_THIS_DIR, "data", "atom_typing_radii.yml"), "r") as handle:
    _ATOM_TYPING_CUTOFFS = yaml.load(handle, Loader=yaml.UnsafeLoader)  # noqa: S506


with open(os.path.join(_THIS_DIR, "data", "li_radii.yml"), "r") as handle:
    _LI_TYPING_CUTOFFS = yaml.load(handle, Loader=yaml.UnsafeLoader)  # noqa: S506


#: :obj:`CutOffDictNN` :
#: Hand-tuned cutoff values for based on the original ones in pymatgen.
VestaCutoffDictNN = CutOffDictNN(cut_off_dict=_VESTA_CUTOFFS)

#: :obj:`CutOffDictNN` :
#: Atomic typing radii.
ATRCutoffDictNN = CutOffDictNN(cut_off_dict=_ATOM_TYPING_CUTOFFS)

#: :obj:`CutOffDictNN` :
#: Lennard-Jones cutoff radii.
LICutoffDictNN = CutOffDictNN(cut_off_dict=_LI_TYPING_CUTOFFS)


__all__ = (
    "get_nx_graph_from_edge_tuples",
    "VestaCutoffDictNN",
    "ATRCutoffDictNN",
    "LICutoffDictNN",
    "get_local_env_method",
    "get_structure_graph",
    "construct_clean_graph",
)


def get_local_env_method(method: str) -> NearNeighbors:
    """Get a local environment method based on its name.

    Args:
        method: Name of the method.

    Returns:
        NearNeighbors: Local environment method.

    Example:
        >>> from structuregraph_helpers import get_local_env_method
        >>> get_local_env_method("voronoi")
        <pymatgen.analysis.local_env.VoronoiNN object at 0x...>
    """
    method = method.lower()

    if method.lower() == "crystalnn":
        # see eq. 15 and 16 in
        # https://pubs.acs.org/doi/full/10.1021/acs.inorgchem.0c02996
        # for the x_diff_weight parameter.
        # in the paper it is called δen and it is set to 3
        # we found better results by lowering this weight
        return CrystalNN(porous_adjustment=True, x_diff_weight=1.5, search_cutoff=4.5)
    if method.lower() == "econnn":
        return EconNN()
    if method.lower() == "brunnernn":
        return BrunnerNN_relative()
    if method.lower() == "minimumdistance":
        return MinimumDistanceNN()
    if method.lower() == "vesta":
        return VestaCutoffDictNN
    if method.lower() == "voronoinn":
        return VoronoiNN()
    if method.lower() == "atr":
        return ATRCutoffDictNN
    if method.lower() == "li":
        return LICutoffDictNN

    return VoronoiNN()


def get_structure_graph(structure: Structure, method: str = "vesta") -> StructureGraph:
    """Get a structure graph for a structure."""
    sg = StructureGraph.with_local_env_strategy(structure, get_local_env_method(method))
    nx.set_node_attributes(
        sg.graph,
        name="idx",
        values=dict(zip(range(len(sg)), range(len(sg)))),
    )
    return sg


def get_nx_graph_from_edge_tuples(edge_tuples: Iterable[Tuple[int, int]]) -> nx.Graph:
    """Create a undirected graph from a list of edge tuples.

    Args:
        edge_tuples: List of edge tuples.

    Returns:
        nx.Graph: Undirected graph.

    Example:
        >>> from structuregraph_helpers import get_nx_graph_from_edge_tuples
        >>> get_nx_graph_from_edge_tuples([(0, 0), (0, 1), (1, 0), (1, 1)])
        Graph(2 nodes, 3 edges)
    """
    graph = nx.Graph()
    graph.add_edges_from(edge_tuples)
    return graph


def construct_clean_graph(
    structure_graph: StructureGraph, multigraph: bool = False, directed: bool = False
) -> nx.Graph:
    """Create a networkx graph with atom numbers and coordination numbers as node attributes.

    .. warning::

        If you choose directed=True, but multigraph=False, there might be fewer
        edges than you intuitively expec as we do not flip the direction
        based on the edge data.

    Args:
        structure_graph (StructureGraph): StructureGraph to convert.
        multigraph (bool): Whether to use return a multigraph.
        directed (bool): Whether to use return adirected graph.

    Returns:
        nx.Graph: Networkx graph.
    """
    if multigraph:
        if directed:
            graph = nx.MultiDiGraph()
        else:
            graph = nx.MultiGraph()
    else:
        if directed:
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()
    for u, v, d in structure_graph.graph.edges(data=True):
        voltage = _voltage(u, v, d["to_jimage"])
        graph.add_edge(u, v, voltage=voltage)
    for node in graph.nodes:

        graph.nodes[node]["specie"] = str(structure_graph.structure[node].specie)
        graph.nodes[node]["specie-cn"] = (
            str(structure_graph.structure[node].specie)
            + "-"
            + str(structure_graph.get_coordination_of_site(node))
        )

    return graph


def _voltage(u, v, to_jimage) -> Tuple[int, int, int]:
    """Voltage is the tuple describing the direction of the edge.

    In simple words, it represents the translation operation.

    Args:
        u (int): Start node.
        v (int): End node.
        to_jimage (Tuple[int, int, int]): Translation operation.

    Returns:
        Tuple[int, int, int]: The voltage of the edge.
    """
    terms = (u, v)
    a_image = (0, 0, 0)
    b_image = (-to_jimage[0], -to_jimage[1], -to_jimage[2])
    imags = (a_image, b_image)
    a_image, b_image = (x for x, _ in sorted(zip(imags, terms), key=lambda x: x[1]))
    return tuple(a_image[i] - b_image[i] for i in range(3))
