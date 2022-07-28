from pymatgen.analysis.graphs import StructureGraph

from structuregraph_helpers.create import VestaCutoffDictNN


def test_vesta_cutoffs(ag_n_structure):
    # The 6 neightbors for silver that the CSD shows seem reasonable.
    # The default cutoffs didn't get this right (https://github.com/kjappelbaum/moffragmentor/issues/61)
    sg = StructureGraph.with_local_env_strategy(ag_n_structure, VestaCutoffDictNN)
    assert len(sg.get_connected_sites(0)) == 6
