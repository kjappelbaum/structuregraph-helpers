"""Command-line interface for StructureGraphHelpers."""
import pprint
from collections import OrderedDict

import click
from pymatgen.core import Structure

from structuregraph_helpers.create import get_structure_graph
from structuregraph_helpers.hash import (
    decorated_graph_hash,
    decorated_no_leaf_hash,
    decorated_scaffold_hash,
    undecorated_graph_hash,
    undecorated_no_leaf_hash,
    undecorated_scaffold_hash,
)

__all__ = ["create_hashes_for_structure"]


def create_hashes_for_structure(structure: Structure, lqg: bool = False) -> dict:
    """Create hashes for a Structure.

    Args:
        structure (Structure): pymatgen Structure
        lqg (bool): If True, computed the hash on the labeled quotient graph.

    Returns:
        dict: Dictionary of hashes for the Structure.
    """
    hash_types = [
        ("undecorated_graph_hash", undecorated_graph_hash),
        ("undecorated_no_leaf_hash", undecorated_no_leaf_hash),
        ("undecorated_scaffold_hash", undecorated_scaffold_hash),
        ("decorated_graph_hash", decorated_graph_hash),
        ("decorated_no_leaf_hash", decorated_no_leaf_hash),
        ("decorated_scaffold_hash", decorated_scaffold_hash),
    ]

    sg = get_structure_graph(structure)
    hashes = OrderedDict()
    for name, hash_func in hash_types:
        hashes[name] = hash_func(sg, lqg=lqg)

    return hashes


@click.command("cli")
@click.argument("structure_file", type=click.Path(exists=True))
@click.option("--lqg", is_flag=True, default=False)
def get_hash(structure_file, lqg):
    structure = Structure.from_file(structure_file)
    hashes = create_hashes_for_structure(structure, lqg)

    pprint.pprint(dict(hashes))  # noqa: T203
