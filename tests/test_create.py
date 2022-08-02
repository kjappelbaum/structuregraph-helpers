import networkx as nx
from pymatgen.analysis.graphs import StructureGraph

from structuregraph_helpers.create import (
    VestaCutoffDictNN,
    construct_clean_graph,
    get_local_env_method,
    get_nx_graph_from_edge_tuples,
)


def test_vesta_cutoffs(ag_n_structure):
    # The 6 neightbors for silver that the CSD shows seem reasonable.
    # The default cutoffs didn't get this right (https://github.com/kjappelbaum/moffragmentor/issues/61)
    sg = StructureGraph.with_local_env_strategy(ag_n_structure, VestaCutoffDictNN)
    assert len(sg.get_connected_sites(0)) == 6
    assert sg == StructureGraph.with_local_env_strategy(
        ag_n_structure, get_local_env_method("vesta")
    )


def test_get_nx_graph_from_edge_tuples():
    edge_tuples = [(0, 0), (0, 1), (1, 0), (1, 1)]
    graph = get_nx_graph_from_edge_tuples(edge_tuples)
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 3  # (0,0), (0,1), (1,1)


def test_construct_clean_graph(bcc_graph):
    """The original edges are: # noqa: D400

    0 0 {'to_jimage': (1, 0, 0)}
    0 0 {'to_jimage': (0, 1, 0)}
    0 1 {'to_jimage': (0, 0, 0)}
    0 1 {'to_jimage': (-1, 0, 0)}
    0 1 {'to_jimage': (-1, -1, 0)}
    0 1 {'to_jimage': (0, -1, 0)}
    0 0 {'to_jimage': (1, 0, 0)}
    0 0 {'to_jimage': (0, 1, 0)}
    0 1 {'to_jimage': (0, 0, 0)}
    0 1 {'to_jimage': (-1, 0, 0)}
    0 1 {'to_jimage': (-1, -1, 0)}
    0 1 {'to_jimage': (0, -1, 0)}
    """
    graph = construct_clean_graph(bcc_graph)

    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 2

    for _, _, d in graph.edges(data=True):
        assert isinstance(d["voltage"], tuple)

    for node in graph.nodes:
        assert isinstance(graph.nodes[node]["specie"], str)
        assert isinstance(graph.nodes[node]["specie-cn"], str)

    graph = construct_clean_graph(bcc_graph, directed=True)

    assert isinstance(graph, nx.DiGraph)
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 2

    graph = construct_clean_graph(bcc_graph, multigraph=True, directed=True)

    assert isinstance(graph, nx.MultiDiGraph)
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 6  # there are duplicates in the original graph
