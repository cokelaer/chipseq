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
import sys
import os
import shutil
import argparse
from pathlib import Path

from sequana_pipetools.options import *

from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog
from sequana_pipetools import SequanaManager

col = Colors()

NAME = "chipseq"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(
            usage=usage,
            prog=prog,
            description="",
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        so = InputOptions()
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline_general")

        pipeline_group.add_argument(
            "--genome-directory", dest="genome_directory", default=".", required=True
        )

        pipeline_group.add_argument(
            "--design-file", dest="design", default="design.csv", required=True,
	   help="""A design file in CSV format with 4 columns named 'type,condition,replicat,sample_name' 
where type must be 'IP' for immunoprecipated or 'Input' for the control, replicate must be a number 1 or 2. 
The 'sample_name' is the prefix of the input fastq file. For example if your file 
is named A_R1_.fastq.fz, sample_name is 'A'"""
        )

        pipeline_group.add_argument(
            "--aligner",
            dest="aligner",
            default="bowtie2",
            choices=["bowtie2"],
            help="a mapper tool. bowtie2 is currently the only aligner",
        )

        pipeline_group.add_argument("--blacklist-file",
		dest="blacklist", help="""a black list file to remove section of the genome. BED3 
			format that is a tabulated file. First column is chromosome name, second and
			 third are the start and stop positions of the regions to remove from the analysis""")

        pipeline_group.add_argument(
            "--genome-size",
            dest="genome_size",
            help="automatically filled from the input fasta file but can be overwritten",
        )

        pipeline_group.add_argument(
            "--do-fingerprints",
            dest="fingerprints",
            help="automatically filled from the input fasta file but can be overwritten",
        )

    def parse_args(self, *args):
        args_list = list(*args)
        if "--from-project" in args_list:
            if len(args_list)>2:
                msg = "WARNING [sequana]: With --from-project option, " + \
                        "pipeline and data-related options will be ignored."
                print(col.error(msg))
            for action in self._actions:
                if action.required is True:
                    action.required = False
        options = super(Options, self).parse_args(*args)
        return options



def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    from sequana_pipetools.options import before_pipeline
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

    # the real stuff is here
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()
    from sequana import logger
    logger.setLevel(options.level)
    logger.name = "sequana_chipseq"


    # fill the config file with input parameters
    if options.from_project is None:
        # fill the config file with input parameters
        cfg = manager.config.config
        cfg.input_directory = os.path.abspath(options.input_directory)
        cfg.input_pattern = options.input_pattern

        cfg.general.genome_directory = os.path.abspath(options.genome_directory)

        # general section
        genome_directory = cfg.general.genome_directory

        p = Path(genome_directory)

        fasta = str(p / p.name) + ".fa"
        if not os.path.exists(fasta):
            logger.error(f"The input fasta file must have the extension .fa and named after you genome directory {p.name}")
            sys.exit(-1)

        if options.genome_size:
            cfg.macs3.genome_size = options.genome_size
        else:
            from sequana import FastA
            f  = FastA(fasta)
            cfg.macs3.genome_size = sum(list(f.get_lengths_as_dict().values()))

        if not os.path.exists(str(p / p.name) + ".gff3") and \
           not os.path.exists(str(p / p.name) + ".gff"):
            logger.error(f"The input gff file must have the extension .gff or .gff3 and named after you genome directory {p.name}")
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


        manager.exists(cfg.input_directory)



    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
