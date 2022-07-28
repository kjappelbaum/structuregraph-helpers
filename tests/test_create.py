from pymatgen.analysis.graphs import StructureGraph

from structuregraph_helpers.create import VestaCutoffDictNN, get_nx_graph_from_edge_tuples


def test_vesta_cutoffs(ag_n_structure):
    # The 6 neightbors for silver that the CSD shows seem reasonable.
    # The default cutoffs didn't get this right (https://github.com/kjappelbaum/moffragmentor/issues/61)
    sg = StructureGraph.with_local_env_strategy(ag_n_structure, VestaCutoffDictNN)
    assert len(sg.get_connected_sites(0)) == 6


def test_get_nx_graph_from_edge_tuples():
    edge_tuples = [(0, 0), (0, 1), (1, 0), (1, 1)]
    graph = get_nx_graph_from_edge_tuples(edge_tuples)
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 3  # (0,0), (0,1), (1,1)
