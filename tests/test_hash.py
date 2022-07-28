from pymatgen.analysis.graphs import StructureGraph
from pymatgen.transformations.standard_transformations import RotationTransformation

from structuregraph_helpers.create import VestaCutoffDictNN
from structuregraph_helpers.hash import (
    decorated_graph_hash,
    decorated_no_leaf_hash,
    decorated_scaffold_hash,
    undecorated_graph_hash,
    undecorated_no_leaf_hash,
    undecorated_scaffold_hash,
)


def test_hash_rotation_invariance(ag_n_structure):
    # decorated graph hash
    sg = StructureGraph.with_local_env_strategy(ag_n_structure, VestaCutoffDictNN)
    original_decorated_graph_hash = decorated_graph_hash(sg)
    original_undecorated_graph_hash = undecorated_graph_hash(sg)
    original_decorated_no_leaf_hash = decorated_no_leaf_hash(sg)
    original_undecorated_no_leaf_hash = undecorated_no_leaf_hash(sg)
    original_decorated_scaffold_hash = decorated_scaffold_hash(sg)
    original_undecorated_scaffold_hash = undecorated_scaffold_hash(sg)

    # rotate structure
    rotation_transformer = RotationTransformation([1, 0, 0], 10)
    rotated_structure = rotation_transformer.apply_transformation(ag_n_structure)
    sg_rotated = StructureGraph.with_local_env_strategy(rotated_structure, VestaCutoffDictNN)
    rotated_decorated_graph_hash = decorated_graph_hash(sg_rotated)
    rotated_undecorated_graph_hash = undecorated_graph_hash(sg_rotated)
    rotated_decorated_no_leaf_hash = decorated_no_leaf_hash(sg_rotated)
    rotated_undecorated_no_leaf_hash = undecorated_no_leaf_hash(sg_rotated)
    rotated_decorated_scaffold_hash = decorated_scaffold_hash(sg_rotated)
    rotated_undecorated_scaffold_hash = undecorated_scaffold_hash(sg_rotated)

    # assert that the hashes are the same
    assert original_decorated_graph_hash == rotated_decorated_graph_hash
    assert original_undecorated_graph_hash == rotated_undecorated_graph_hash
    assert original_decorated_no_leaf_hash == rotated_decorated_no_leaf_hash
    assert original_undecorated_no_leaf_hash == rotated_undecorated_no_leaf_hash
    assert original_decorated_scaffold_hash == rotated_decorated_scaffold_hash
    assert original_undecorated_scaffold_hash == rotated_undecorated_scaffold_hash


def test_hash_matches(mof_74_zn, mof_74_zr, mof_74_zr_nh2):
    """Taken some checks from the mofchecker test suite."""
    mof_74_zn_sg = StructureGraph.with_local_env_strategy(mof_74_zn, VestaCutoffDictNN)
    mof_74_zr_sg = StructureGraph.with_local_env_strategy(mof_74_zr, VestaCutoffDictNN)
    mof_74_zr_nh2_sg = StructureGraph.with_local_env_strategy(mof_74_zr_nh2, VestaCutoffDictNN)

    mof_74_zn_hash = decorated_graph_hash(mof_74_zn_sg)
    mof_74_zr_hash = decorated_graph_hash(mof_74_zr_sg)
    mof_74_zr_nh2_hash = decorated_graph_hash(mof_74_zr_nh2_sg)

    assert mof_74_zn_hash != mof_74_zr_hash
    assert mof_74_zn_hash != mof_74_zr_nh2_hash
    assert mof_74_zr_hash != mof_74_zr_nh2_hash

    mof_74_zn_scaffold_hash = decorated_scaffold_hash(mof_74_zn_sg)
    mof_74_zr_scaffold_hash = decorated_scaffold_hash(mof_74_zr_sg)
    mof_74_zr_nh2_scaffold_hash = decorated_scaffold_hash(mof_74_zr_nh2_sg)

    assert mof_74_zn_scaffold_hash != mof_74_zr_scaffold_hash
    assert mof_74_zn_scaffold_hash != mof_74_zr_nh2_scaffold_hash
    assert mof_74_zr_scaffold_hash == mof_74_zr_nh2_scaffold_hash

    mof_74_zn_undecorated_hash = undecorated_graph_hash(mof_74_zn_sg)
    mof_74_zr_undecorated_hash = undecorated_graph_hash(mof_74_zr_sg)
    mof_74_zr_nh2_undecorated_hash = undecorated_graph_hash(mof_74_zr_nh2_sg)

    assert mof_74_zn_undecorated_hash == mof_74_zr_undecorated_hash
    assert mof_74_zn_undecorated_hash != mof_74_zr_nh2_undecorated_hash
    assert mof_74_zr_undecorated_hash != mof_74_zr_nh2_undecorated_hash

    mof_74_zn_undecorated_scaffold_hash = undecorated_scaffold_hash(mof_74_zn_sg)
    mof_74_zr_undecorated_scaffold_hash = undecorated_scaffold_hash(mof_74_zr_sg)
    mof_74_zr_nh2_undecorated_scaffold_hash = undecorated_scaffold_hash(mof_74_zr_nh2_sg)

    assert mof_74_zn_undecorated_scaffold_hash == mof_74_zr_undecorated_scaffold_hash
    assert mof_74_zn_undecorated_scaffold_hash == mof_74_zr_nh2_undecorated_scaffold_hash
    assert mof_74_zr_undecorated_scaffold_hash == mof_74_zr_nh2_undecorated_scaffold_hash
