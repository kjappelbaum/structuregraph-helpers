import os
import subprocess
from glob import glob
from pathlib import Path

import click
import numpy as np

SLURM_SUBMISSION_TEMPLATE = """#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={job_name}.out
#SBATCH --error={job_name}.err
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=3GB

conda activate mofdscribe
python compute_hashes.py --indir {indir} --outdir {outdir} --start {start} --end {end}
"""


@click.command("cli")
@click.argument("indir", type=click.Path(exists=True))
@click.argument("outdir")
def cli(indir, outdir):
    ALL_STRUCTURES = glob(os.path.join(indir, "*.cif"))
    CHUNK_SIZE = 1000
    name = Path(indir).stem
    for start in range(0, len(ALL_STRUCTURES), CHUNK_SIZE):
        end = start + CHUNK_SIZE
        job_name = f"hasher_{name}_{start}_{end}"

        with open(f"{job_name}.slurm", "w") as f:
            f.write(
                SLURM_SUBMISSION_TEMPLATE.format(
                    indir=indir, outdir=outdir, start=start, end=end, job_name=job_name
                )
            )
        subprocess.run(["sbatch", f"{job_name}.slurm"])


if __name__ == "__main__":
    cli()
