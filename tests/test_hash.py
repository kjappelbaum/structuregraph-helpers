from structuregraph_helpers.hash import (
    decorated_graph_hash,
    undecorated_graph_hash,
    decorated_no_leaf_hash,
    undecorated_no_leaf_hash,
)
from structuregraph_helpers.create import VestaCutoffDictNN
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.transformations.standard_transformations import RotationTransformation


def test_hash_rotation_invariance(ag_n_structure):
    # decorated graph hash
    sg = StructureGraph.with_local_env_strategy(ag_n_structure, VestaCutoffDictNN)
    original_decorated_graph_hash = decorated_graph_hash(sg)
    original_undecorated_graph_hash = undecorated_graph_hash(sg)
    original_decorated_no_leaf_hash = decorated_no_leaf_hash(sg)
    original_undecorated_no_leaf_hash = undecorated_no_leaf_hash(sg)

    # rotate structure
    rotation_transformer = RotationTransformation([1, 0, 0], 10)
    rotated_structure = rotation_transformer.apply_transformation(ag_n_structure)
    sg_rotated = StructureGraph.with_local_env_strategy(rotated_structure, VestaCutoffDictNN)
    rotated_decorated_graph_hash = decorated_graph_hash(sg_rotated)
    rotated_undecorated_graph_hash = undecorated_graph_hash(sg_rotated)
    rotated_decorated_no_leaf_hash = decorated_no_leaf_hash(sg_rotated)
    rotated_undecorated_no_leaf_hash = undecorated_no_leaf_hash(sg_rotated)

    # assert that the hashes are the same
    assert original_decorated_graph_hash == rotated_decorated_graph_hash
    assert original_undecorated_graph_hash == rotated_undecorated_graph_hash
    assert original_decorated_no_leaf_hash == rotated_decorated_no_leaf_hash
    assert original_undecorated_no_leaf_hash == rotated_undecorated_no_leaf_hash
