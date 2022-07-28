import os

import pytest
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.core import Lattice, Structure

from structuregraph_helpers.create import VestaCutoffDictNN

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="function")
def bcc_graph():
    """Return example structure graph taken from pymatgen tests."""
    structure = Structure(Lattice.tetragonal(5.0, 50.0), ["H", "He"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    bc_square_sg_r = StructureGraph.with_empty_graph(
        structure, edge_weight_name="", edge_weight_units=""
    )
    bc_square_sg_r.add_edge(0, 0, from_jimage=(0, 0, 0), to_jimage=(1, 0, 0))
    bc_square_sg_r.add_edge(0, 0, from_jimage=(0, 0, 0), to_jimage=(-1, 0, 0))
    bc_square_sg_r.add_edge(0, 0, from_jimage=(0, 0, 0), to_jimage=(0, 1, 0))
    bc_square_sg_r.add_edge(0, 0, from_jimage=(0, 0, 0), to_jimage=(0, -1, 0))
    bc_square_sg_r.add_edge(0, 1, from_jimage=(0, 0, 0), to_jimage=(0, 0, 0))
    bc_square_sg_r.add_edge(1, 0, from_jimage=(-1, 0, 0), to_jimage=(0, 0, 0))
    bc_square_sg_r.add_edge(1, 0, from_jimage=(-1, -1, 0), to_jimage=(0, 0, 0))
    bc_square_sg_r.add_edge(1, 0, from_jimage=(0, -1, 0), to_jimage=(0, 0, 0))

    return bc_square_sg_r


@pytest.fixture(scope="session")
def ag_n_structure():
    """https://www.ccdc.cam.ac.uk/structures/Search?Ccdcid=PAVLOO."""
    return Structure.from_file(os.path.join(_THIS_DIR, "test_files", "RSM0956.cif"))


@pytest.fixture(scope="session")
def floating_hkust():
    return Structure.from_file(os.path.join(_THIS_DIR, "test_files", "HKUST_floating.cif"))


@pytest.fixture(scope="session")
def floating_hkust_graph():
    return StructureGraph.with_local_env_strategy(
        Structure.from_file(os.path.join(_THIS_DIR, "test_files", "HKUST_floating.cif")),
        VestaCutoffDictNN,
    )


@pytest.fixture(scope="session")
def hkust_graph():
    return StructureGraph.with_local_env_strategy(
        Structure.from_file(os.path.join(_THIS_DIR, "test_files", "HKUST-1.cif")),
        VestaCutoffDictNN,
    )


@pytest.fixture(scope="session")
def mof_74_zr():
    return Structure.from_file(os.path.join(_THIS_DIR, "test_files", "MOF-74-Zr.cif"))


@pytest.fixture(scope="session")
def mof_74_zn():
    return Structure.from_file(os.path.join(_THIS_DIR, "test_files", "MOF-74-Zn.cif"))


@pytest.fixture(scope="session")
def mof_74_zr_nh2():
    return Structure.from_file(os.path.join(_THIS_DIR, "test_files", "MOF-74-Zr-NH2.cif"))
