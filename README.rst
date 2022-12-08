This is is the **chipseq** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project

:Overview: TODO 
:Input: TODO
:Output: TODO
:Status: draft
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

You must install Sequana first::

    pip install sequana

Then, just install this package::

    pip install sequana_chipseq


Usage
~~~~~

::

    sequana_pipelines_chipseq --help
    sequana_pipelines_chipseq --input-directory DATAPATH 

This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd chipseq
    sh chipseq.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s chipseq.rules -c config.yaml --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- idr This python package is not on pypi. Manual installation is required. Instructions are here:
https://github.com/nboley/idr but we also provide a singularity in https://damona.readthedocs.io

.. image:: https://raw.githubusercontent.com/sequana/sequana_chipseq/master/sequana_pipelines/chipseq/dag.png


Details
~~~~~~~~~

This pipeline runs **chipseq** in parallel on the input fastq files (paired or not). 
A brief sequana summary report is also produced.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_chipseq/master/sequana_pipelines/chipseq/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.0.1     **First release.**
========= ====================================================================


