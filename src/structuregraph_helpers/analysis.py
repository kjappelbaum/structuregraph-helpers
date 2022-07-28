"""Helpers for analysing structure graphs."""
from typing import List

import networkx as nx
from pymatgen.analysis.dimensionality import get_dimensionality_larsen
from pymatgen.analysis.graphs import StructureGraph

__all__ = ["get_structure_graph_dimensionality", "get_leaf_nodes"]


def get_leaf_nodes(graph: nx.Graph) -> List[int]:
    """For a graph, return the indices of the leaf nodes.

    Args:
        graph (nx.Graph): networkx graph

    Returns:
        List[int]: indices of leaf nodes
    """
    return [node for node in graph.nodes() if graph.degree(node) == 1]


def get_structure_graph_dimensionality(structure_graph: StructureGraph) -> int:
    """Use Larsen's algorithm to compute the dimensionality.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph

    Returns:
        int: Dimensionality of the StructureGraph

    Example:
        >>> from structuregraph_helpers import get_structure_graph_dimensionality
        >>> get_structure_graph_dimensionality(structure_graph)
        3

    References:
        [Larsen] `Larsen, P. M.; Pandey, M.; Strange, M.; Jacobsen,
            K. W. Definition of a Scoring Parameter to Identify Low-Dimensional
            Materials Components. Physical Review Materials, 2019, 3.
            <https://doi.org/10.1103/physrevmaterials.3.034003>`_
    """
    return get_dimensionality_larsen(structure_graph)


def get_cn(structure_graph: StructureGraph, site_index: int) -> int:
    """Get the coordination number of a site.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph
        site_index (int): index of the site

    Returns:
        int: coordination number of the site

    Example:
        >>> from structuregraph_helpers.analysis import get_cn
        >>> get_cn(structure_graph, 0)
        3
    """
    return len(structure_graph.get_connected_sites(site_index))
