import numpy as np
from pymatgen.analysis.graphs import MoleculeGraph
from pymatgen.core import Molecule

from structuregraph_helpers.subgraph import get_subgraphs_as_molecules


def test_get_subgraphs_as_molecules(floating_hkust_graph):
    mols, graphs, indices, centers, coordinates = get_subgraphs_as_molecules(floating_hkust_graph)
    for mol in mols:
        assert isinstance(mol, Molecule)

    assert len(mols) == 1
    assert "H" in str(mols[0].composition)
    for graph in graphs:
        assert isinstance(graph, MoleculeGraph)

    for idx in indices:
        assert len(idx) == 1

    for center in centers:
        assert len(center) == 3

    for coord in coordinates:
        assert isinstance(coord, np.ndarray)
