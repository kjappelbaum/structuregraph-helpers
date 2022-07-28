from structuregraph_helpers.analysis import get_dimensionality_larsen, get_leaf_nodes


def test_get_dimensionality_larsen(bcc_graph):
    assert get_dimensionality_larsen(bcc_graph) == 2


def test_get_leaf_nodes(bcc_graph):
    assert get_leaf_nodes(bcc_graph.graph) == []
