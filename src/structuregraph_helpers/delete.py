"""Helpers for deleting parts of graphs."""
from collections import defaultdict
from copy import deepcopy
from typing import Iterable, Tuple

import networkx as nx
import numpy as np
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.core import Structure

from .analysis import get_leaf_nodes

__all__ = ("remove_all_nodes_not_in_indices",)


def remove_all_nodes_not_in_indices(graph: StructureGraph, indices: Iterable[int]) -> None:
    """Remove all nodes that are *not* in the given indices from the StructureGraph.

    .. note::

        The StructureGraph is modified in place.

    Args:
        graph (StructureGraph): pymatgen StructureGraph
        indices (Iterable[int]): Indices of nodes to keep
    """
    to_delete = [i for i in range(len(graph)) if i not in indices]
    graph.structure = Structure.from_sites(graph.structure.sites)
    graph.remove_nodes(to_delete)


def get_structure_graph_without_leaf_nodes(
    structure_graph: StructureGraph,
) -> Tuple[StructureGraph, nx.Graph]:
    """
    Return a StructureGraph without leaf nodes.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph

    Returns:
        StructureGraph: StructureGraph without leaf nodes
        nx.Graph: Graph without leaf nodes

    Example:
        >>> from structuregraph_helpers import get_structure_graph_without_leaf_nodes
        >>> get_structure_graph_without_leaf_nodes(structure_graph)
        (StructureGraph, nx.Graph)
    """
    leaf_sites = get_leaf_nodes(structure_graph.graph)

    graph_ = structure_graph.__copy__()
    graph_.structure = Structure.from_sites(graph_.structure.sites)
    graph_.remove_nodes(leaf_sites)

    edges = {(u, v) for u, v, _ in graph_.graph.edges(keys=False, data=True)}
    graph = nx.Graph()
    graph.add_edges_from(edges)
    for node in graph.nodes:

        graph.nodes[node]["specie"] = str(graph_.structure[node].specie)
        graph.nodes[node]["specie-cn"] = (
            str(graph_.structure[node].specie)
            + "-"
            + str(structure_graph.get_coordination_of_site(node))
        )

    return graph_, graph


def get_structure_graph_with_broken_bridges(
    structure_graph: StructureGraph,
) -> Tuple[StructureGraph, nx.Graph]:
    """
    Return a StructureGraph without the small subgraphs one obtains after breaking edges.

    In chemical terms, this is supposed to remove hydrogen atoms and functional groups.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph.

    Returns:
        StructureGraph: StructureGraph without subgraphs connected via bridges.
        nx.Graph: Graph without subgraphs connected via bridges.

    Example:
        >>> from structuregraph_helpers import get_structure_graph_with_broken_bridges
        >>> get_structure_graph_with_broken_bridges(structure_graph)
        (StructureGraph, nx.Graph)
    """
    g = nx.DiGraph(deepcopy(structure_graph.graph)).to_undirected()
    bridges = _generate_bridges(g)
    for k, v in bridges.items():
        for neighbor in v:
            g.remove_edge(k, neighbor)

    subgraphs = [sg for sg in nx.connected_components(g)]

    subgraphs_len = [len(sg) for sg in subgraphs]
    longest_subgraph = np.argmax(subgraphs_len)

    # going via remove nodes seems easier than removing the edges
    # (for which we'd need to deal with the periodic attributes)
    to_delete = []
    for i, sg in enumerate(subgraphs):
        if i != longest_subgraph:
            to_delete.extend(sg)

    graph_ = structure_graph.__copy__()
    graph_.structure = Structure.from_sites(graph_.structure.sites)
    graph_.remove_nodes(to_delete)

    edges = {(u, v) for u, v, d in graph_.graph.edges(keys=False, data=True)}
    graph = nx.Graph()
    graph.add_edges_from(edges)
    for node in graph.nodes:

        graph.nodes[node]["specie"] = str(graph_.structure[node].specie)
        graph.nodes[node]["specie-cn"] = (
            str(graph_.structure[node].specie)
            + "-"
            + str(structure_graph.get_coordination_of_site(node))
        )

    return graph_, graph


def _generate_bridges(nx_graph: nx.Graph) -> dict:
    """Find all bridges in a graph."""
    bridges = list(nx.bridges(nx_graph))

    bridges_dict = defaultdict(list)
    for key, value in bridges:
        bridges_dict[key].append(value)
    return dict(bridges_dict)
