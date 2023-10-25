
.. image:: https://badge.fury.io/py/sequana-chipseq.svg
     :target: https://pypi.python.org/pypi/sequana_chipseq

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI

.. image:: https://github.com/sequana/chipseq/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/chipseq/actions/    


.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C3.10-blue.svg
    :target: https://pypi.python.org/pypi/sequana
    :alt: Python 3.8 | 3.9 | 3.10


This is is the **chipseq** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project

:Overview: ChIP-seq pipeline to detect peaks using IDR statistics
:Input: Set of fastq files and a design file
:Output: HTML reports and various plots and annotation files
:Status: production
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

Just install this package using Python **pip** software::

    pip install sequana_chipseq --upgrade


Usage
~~~~~

::

    sequana_chipseq --help
    sequana_chipseq --input-directory DATAPATH 

This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd chipseq
    sh chipseq.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s chipseq.rules -c config.yaml --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/main/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipeline requires the following executable(s):

- idr This python package is not on pypi. Manual installation is required. Instructions are here:
https://github.com/nboley/idr but we also provide a singularity in https://damona.readthedocs.io

.. image:: https://raw.githubusercontent.com/sequana/chipseq/main/sequana_pipelines/chipseq/dag.png
.. image:: https://raw.githubusercontent.com/sequana/chipseq/main/sequana_pipelines/chipseq/dag_complete.png


Details
~~~~~~~~~

This pipeline runs **chipseq** in parallel on the input fastq files (paired or not). 
A brief sequana summary report is also produced.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/chipseq/main/sequana_pipelines/chipseq/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.10.0    * Fix design in case of samples that starts with same prefix
          * Include final IDR plots and tables
          * Fix containers and wrappers in the config file
          * Better HTML report
0.9.1     * Fix requirements and setup.py (remove wrong idr package)
0.9.0     * use latest wrappers and apptainer (for rulegraph)
0.8.0     **First release.**
========= ====================================================================


