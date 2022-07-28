from structuregraph_helpers.delete import remove_all_nodes_not_in_indices


def test_remove_all_nodes_not_in_indices(bcc_graph):
    remove_all_nodes_not_in_indices(bcc_graph, [1])
    assert len(bcc_graph.graph.nodes) == 1

    assert len(bcc_graph.graph.edges) == 0
