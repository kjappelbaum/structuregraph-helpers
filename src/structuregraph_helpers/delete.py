"""Helpers for deleting parts of graphs."""
from typing import Iterable

from pymatgen.analysis.graphs import StructureGraph
from pymatgen.core import Structure

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
