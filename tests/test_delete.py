import networkx as nx
from pymatgen.analysis.graphs import StructureGraph

from structuregraph_helpers.delete import (
    get_structure_graph_without_leaf_nodes,
    remove_all_nodes_not_in_indices,
)


def test_remove_all_nodes_not_in_indices(bcc_graph):
    remove_all_nodes_not_in_indices(bcc_graph, [1])
    assert len(bcc_graph.graph.nodes) == 1

    assert len(bcc_graph.graph.edges) == 0


def test_get_structure_graph_without_leaf_nodes(hkust_graph):
    # Make sure that all the Hs are removed
    new_sg, new_g = get_structure_graph_without_leaf_nodes(hkust_graph)
    assert isinstance(new_sg, StructureGraph)
    assert isinstance(new_g, nx.Graph)

    new_comp = dict(new_sg.structure.composition)
    new_comp = {str(k): v for k, v in new_comp.items()}

    assert "H" not in new_comp
    assert new_comp["Cu"] == 48
    assert new_comp["O"] == 192
    assert new_comp["C"] == 288.0
