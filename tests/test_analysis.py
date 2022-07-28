from pymatgen.analysis.graphs import StructureGraph

from structuregraph_helpers.analysis import get_cn, get_dimensionality_larsen, get_leaf_nodes
from structuregraph_helpers.create import VestaCutoffDictNN


def test_get_dimensionality_larsen(bcc_graph):
    assert get_dimensionality_larsen(bcc_graph) == 2


def test_get_leaf_nodes(bcc_graph):
    assert get_leaf_nodes(bcc_graph.graph) == []


def test_get_cn(ag_n_structure):
    sg = StructureGraph.with_local_env_strategy(ag_n_structure, VestaCutoffDictNN)
    assert get_cn(sg, 0) == 6
