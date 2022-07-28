"""Helpers for creating graphs."""
import os
from typing import Iterable, Tuple

import networkx as nx
import yaml
from pymatgen.analysis.local_env import CutOffDictNN

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(_THIS_DIR, "data", "tuned_vesta.yml"), "r", encoding="utf8") as handle:
    _VESTA_CUTOFFS = yaml.load(handle, Loader=yaml.UnsafeLoader)  # noqa: S506

#: :obj:`CutOffDictNN` :
#: Hand-tuned cutoff values for based on the original ones in pymatgen.
VestaCutoffDictNN = CutOffDictNN(cut_off_dict=_VESTA_CUTOFFS)

__all__ = ("get_nx_graph_from_edge_tuples", "VestaCutoffDictNN")


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
