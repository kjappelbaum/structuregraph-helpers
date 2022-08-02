"""Command-line interface for StructureGraphHelpers."""
import concurrent.futures
import os
import pprint
from collections import OrderedDict
from functools import partial
from glob import glob
from pathlib import Path
from typing import Union

import click
import numpy as np
from loguru import logger
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
from structuregraph_helpers.utils import dump_json

__all__ = ["create_hashes_for_structure"]


def create_hashes_for_structure(
    structure: Union[Structure, os.PathLike], lqg: bool = False
) -> dict:
    """Create hashes for a Structure.

    Args:
        structure (Union[Structure, os.PathLike]): pymatgen Structure
        lqg (bool): If True, computed the hash on the labeled quotient graph.

    Returns:
        dict: Dictionary of hashes for the Structure.
    """
    hashes = OrderedDict()
    hash_types = [
        ("undecorated_graph_hash", undecorated_graph_hash),
        ("undecorated_no_leaf_hash", undecorated_no_leaf_hash),
        ("undecorated_scaffold_hash", undecorated_scaffold_hash),
        ("decorated_graph_hash", decorated_graph_hash),
        ("decorated_no_leaf_hash", decorated_no_leaf_hash),
        ("decorated_scaffold_hash", decorated_scaffold_hash),
    ]
    try:
        if isinstance(structure, (os.PathLike, str, Path)):
            structure = Structure.from_file(structure)

        sg = get_structure_graph(structure)

        for name, hash_func in hash_types:
            hashes[name] = hash_func(sg, lqg=lqg)
    except Exception as e:
        logger.error(f"Error {e} computing hashes for {structure}")
        for name, hash_func in hash_types:
            hashes[name] = np.nan

    return hashes


def compute_hashes_for_folder(
    folder: os.PathLike, outname: os.PathLike, lqg: bool = False, n_jobs: int = 1
) -> dict:
    """Create hashes for all CIF files in a folder.

    Args:
        folder (os.PathLike): Path to folder containing CIF files.
        outname (os.PathLike): Path to output file.
        lqg (bool): If True, computed the hash on the labeled quotient graph.
        n_jobs (int): Number of jobs to run in parallel.

    Returns:
        dict: Dictionary of hashes for the Structure.
    """
    hashes = OrderedDict()
    cif_files = glob(os.path.join(folder, "*.cif"))

    curried_func = partial(create_hashes_for_structure, lqg=lqg)

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        for res, file in zip(executor.map(curried_func, cif_files), cif_files):
            name = Path(file).stem
            hashes[name] = res

    if outname is not None:
        dump_json(hashes, outname)
    return hashes


@click.command("cli")
@click.argument("structure_file", type=click.Path(exists=True))
@click.option("--lqg", is_flag=True, default=False)
def get_hash(structure_file, lqg):
    structure = Structure.from_file(structure_file)
    hashes = create_hashes_for_structure(structure, lqg)

    pprint.pprint(dict(hashes))  # noqa: T203


@click.command("cli")
@click.argument("indir", type=click.Path(exists=True))
@click.argument("outname", type=click.Path())
@click.option("--n-jobs", type=int, default=1)
@click.option("--lqg", is_flag=True, default=False)
def get_hashes(indir, outname, n_jobs, lqg):
    hashes = compute_hashes_for_folder(indir, outname, lqg, n_jobs)
    dump_json(hashes, outname)
