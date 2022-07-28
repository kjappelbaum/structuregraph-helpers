import os

import pytest
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.core import Lattice, Structure

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def bcc_graph():
    """Example strcture graph taken from pymatgen tests."""
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
    """https://www.ccdc.cam.ac.uk/structures/Search?Ccdcid=PAVLOO"""
    return Structure.from_file(os.path.join(_THIS_DIR, "test_files", "RSM0956.cif"))
