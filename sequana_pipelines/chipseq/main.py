#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os
import shutil
import sys

import rich_click as click
from sequana_pipetools import SequanaManager
from sequana_pipetools.options import *
NAME = "chipseq"


help = init_click(
    NAME,
    groups={
        "Pipeline Specific": [
            "--aligner-choice",
            "--genome-directory",
            "--design-file",
            "--blacklist-file",
            "--genome-size",
            "--do-fingerprints",
        ],
    },
)


@click.command(context_settings=help)
@include_options_from(ClickInputOptions)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickGeneralOptions)
@click.option("--genome-directory", "genome_directory", default=".", required=True)
@click.option(
    "--design-file",
    "design",
    default="design.csv",
    required=True,
    help="""A design file in CSV format with 4 columns named 'type,condition,replicat,sample_name'
where type must be 'IP' for immunoprecipated or 'Input' for the control, replicate must be a number 1 or 2.
The 'sample_name' is the prefix of the input fastq file. For example if your file
is named A_R1_.fastq.fz, sample_name is 'A'""",
)
@click.option(
    "--aligner-choice",
    "aligner",
    default="bowtie2",
    show_default=True,
    type=click.Choice(["bowtie2"]),
    help="a mapper tool. bowtie2 is currently the only aligner",
)
@click.option(
    "--blacklist-file",
    "blacklist",
    help="""a black list file to remove section of the genome. BED3
			format that is a tabulated file. First column is chromosome name, second and
			 third are the start and stop positions of the regions to remove from the analysis""",
)
@click.option(
    "--genome-size",
    "genome_size",
    type=click.Path(dir_okay=True, file_okay=False),
    help="automatically filled from the input fasta file but can be overwritten",
)
@click.option(
    "--do-fingerprints",
    "fingerprints",
    help="automatically filled from the input fasta file but can be overwritten",
)
def main(**options):

    if options["from_project"]:
        click.echo("--from-project Not yet implemented")
        sys.exit(1)

    # the real stuff is here
    manager = SequanaManager(options, NAME)
    manager.setup()

    # aliases
    options = manager.options
    cfg = manager.config.config

    from sequana_pipetools import logger

    logger.setLevel(options.level)
    logger.name = "sequana_chipseq"

    manager.fill_data_options()

    cfg.general.genome_directory = os.path.abspath(options.genome_directory)

    # general section
    genome_directory = cfg.general.genome_directory
    from pathlib import Path

    p = Path(genome_directory)

    fasta = str(p / p.name) + ".fa"
    if not os.path.exists(fasta):
        logger.error(f"The input fasta file must have the extension .fa and named after you genome directory {p.name}")
        sys.exit(-1)

    if options.genome_size:
        cfg.macs3.genome_size = options.genome_size
    else:
        from sequana import FastA

        f = FastA(fasta)
        cfg.macs3.genome_size = sum(list(f.get_lengths_as_dict().values()))

    if not os.path.exists(str(p / p.name) + ".gff3") and not os.path.exists(str(p / p.name) + ".gff"):
        logger.error(
            f"The input gff file must have the extension .gff or .gff3 and named after you genome directory {p.name}"
        )
        sys.exit(-1)

    cfg.general.aligner = options.aligner

    if options.blacklist:
        cfg.remove_blacklist.blacklist_file = options.blacklist
        cfg.remove_blacklist.do = True
    else:
        cfg.remove_blacklist.do = False

    if options.fingerprints:
        cfg.fingerprints.do = True
    else:
        cfg.fingerprints.do = False

    # design file
    from sequana_pipelines.chipseq.tools import ChIPExpDesign

    cfg.general.design_file = Path(options.design).name
    shutil.copy(options.design, options.workdir)

    d = ChIPExpDesign(options.design)
    logger.info(f"Found {len(d.conditions)} conditions in the design")

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
