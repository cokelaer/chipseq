
.. image:: https://badge.fury.io/py/sequana-chipseq.svg
     :target: https://pypi.python.org/pypi/sequana_chipseq

.. image:: https://github.com/sequana/chipseq/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/chipseq/actions/workflows/main.yml

.. image:: https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg
    :target: https://pypi.python.org/pypi/sequana
    :alt: Python 3.10 | 3.11 | 3.12

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI

This is the **chipseq** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project.

:Overview: ChIP-seq pipeline from raw reads to peaks, IDR statistics, and functional annotation
:Input: Paired or single-end FastQ files and a CSV experimental design file
:Output: HTML summary report, narrow/broad peak files, IDR statistics, bigwig tracks, annotation tables, and IGV session file
:Status: Production
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi.org/10.21105/joss.00352


.. image:: sequana_pipelines/chipseq/dag.png
   :width: 100%

.. image:: sequana_pipelines/chipseq/dag_complete.png
   :width: 100%


Installation
~~~~~~~~~~~~

::

    pip install sequana_chipseq --upgrade

You will also need the third-party tools listed under Requirements below.


Quick Start
~~~~~~~~~~~

**1. Prepare a design file** ``design.csv``::

    type,condition,replicat,sample_name
    IP,EXP1,1,IP_EXP1_rep1
    IP,EXP1,2,IP_EXP1_rep2
    Input,EXP1,1,Input_EXP1

- ``type`` must be ``IP`` (immunoprecipitated) or ``Input`` (control).
- ``sample_name`` must match the prefix of the corresponding FastQ file
  (e.g. ``IP_EXP1_rep1`` matches ``IP_EXP1_rep1_R1_.fastq.gz``).
- At least two IP replicates per condition are required for IDR analysis.

**2. Prepare a genome directory** named after the genome, containing:

- ``<name>.fa`` — reference genome FASTA
- ``<name>.gff`` or ``<name>.gff3`` — gene annotation

Example::

    ecoli_MG1655/
    ├── ecoli_MG1655.fa
    └── ecoli_MG1655.gff

**3. Set up the pipeline**::

    sequana_chipseq \
        --input-directory DATAPATH \
        --genome-directory /path/to/ecoli_MG1655 \
        --design-file design.csv

**4. Run the pipeline**::

    cd chipseq
    sh chipseq.sh


Usage
~~~~~

::

    sequana_chipseq --help

Key pipeline-specific options:

``--genome-directory``
    Path to the genome directory (must contain ``<name>.fa`` and ``<name>.gff``).

``--design-file``
    CSV experimental design file (see Quick Start above).

``--aligner-choice``
    Aligner to use. Currently only ``bowtie2`` is supported.

``--blacklist-file``
    BED3 file of genomic regions to exclude from analysis (tab-separated:
    chromosome, start, end).

``--genome-size``
    Effective genome size for macs3 peak calling. Automatically computed from
    the FASTA file if not provided; override with a plain integer.

``--do-fingerprints``
    Enable ``plotFingerprint`` QC to assess ChIP enrichment quality.

Run on a SLURM cluster::

    cd chipseq
    sbatch chipseq.sh

Or drive Snakemake directly::

    snakemake -s chipseq.rules --cores 4 --stats stats.txt


Usage with Apptainer
~~~~~~~~~~~~~~~~~~~~~

Run every tool inside pre-built containers — no local tool installation needed::

    sequana_chipseq \
        --input-directory DATAPATH \
        --genome-directory /path/to/genome \
        --design-file design.csv \
        --use-apptainer

Store images in a shared location to avoid re-downloading::

    sequana_chipseq ... --use-apptainer --apptainer-prefix ~/.sequana/apptainers

Then run as usual::

    cd chipseq
    sh chipseq.sh


Requirements
~~~~~~~~~~~~

The following tools must be available (install via conda/bioconda)::

    mamba env create -f environment.yml

- **bowtie2** — read alignment
- **fastp** — adapter trimming and quality filtering
- **fastqc** — per-read quality control
- **samtools** — BAM sorting, indexing, and flagstat
- **bedtools** — bedGraph generation from BAM files (``genomeCoverageBed``)
- **ucsc-bedgraphtobigwig** — bedGraph to bigWig conversion (``bedGraphToBigWig``)
- **deeptools** — fingerprint QC (``plotFingerprint``) and multi-sample bigwig summary (``multiBigwigSummary``)
- **macs3** — narrow and broad peak calling
- **homer** — peak annotation (``annotatePeaks.pl``)
- **idr** — Irreproducibility Discovery Rate between replicates (installed from
  `sequana/idr <https://github.com/sequana/idr>`_ fork via pip; the upstream
  bioconda package is Python 3.10-only)
- **multiqc** — aggregated QC report


Pipeline overview
~~~~~~~~~~~~~~~~~

1. **Trimming** — fastp removes low-quality reads and adapters.
2. **QC** — FastQC on raw and cleaned reads.
3. **Alignment** — bowtie2 maps reads to the reference genome.
4. **[Optional] Mark duplicates** — Picard marks PCR duplicates.
5. **[Optional] Blacklist removal** — bedtools removes artefact-prone regions.
6. **bigwig** — per-sample coverage tracks for genome browsers (bedtools ``genomeCoverageBed`` → UCSC ``bedGraphToBigWig``); an IGV session file (``igv.xml``) is generated to preload all tracks.
7. **[Optional] Fingerprints** — plotFingerprint QC to assess ChIP enrichment.
8. **Phantom peak** — strand cross-correlation analysis (NSC, RSC, Qtag scores).
9. **Peak calling** — macs3 detects narrow and broad peaks for each IP vs Input pair.
10. **FRiP** — Fraction of Reads in Peaks per sample and comparison.
11. **IDR** — Irreproducibility Discovery Rate on true replicates, pseudo-replicates, and self-pseudo-replicates.
12. **Annotation** — homer annotates peaks relative to genomic features.
13. **MultiQC** — aggregated QC across all samples.
14. **HTML report** — summary with phantom peaks, FRiP plots, IDR tables, and annotation plots.


Configuration
~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/chipseq/main/sequana_pipelines/chipseq/config.yaml>`_.
Key sections:

- ``general`` — aligner choice and genome directory path
- ``fastp`` — trimming options (length, quality, adapters)
- ``fastqc`` — FastQC options and threads
- ``bowtie2_mapping`` / ``bowtie2_index`` — mapping options, threads, memory
- ``macs3`` — peak calling parameters (genome size, bandwidth, q-value, broad cutoff)
- ``idr`` — IDR thresholds, rank metric, number of pseudo-replicates
- ``fingerprints`` — enable/disable and number of bins
- ``mark_duplicates`` — enable/disable PCR duplicate marking
- ``remove_blacklist`` — enable/disable and path to BED blacklist
- ``trimming`` — enable/disable read trimming and choice of trimming tool
- ``phantom`` — use SPP (``use_spp: true``) instead of the built-in sequana phantom-peak detection
- ``igv`` — enable/disable generation of the IGV session file (``igv.xml``)
- ``multiqc`` — MultiQC options


Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.12.0    * Fix ``macs3``, ``self_pseudo_replicate_peaks``, and
            ``pseudo_replicate_peaks`` rules: macs3 exits non-zero on sparse
            CI data; added ``|| true`` + conditional ``touch`` so the pipeline
            continues and downstream rules handle empty peak files gracefully
          * Add ``container: sequana_tools`` to all macs3 rules so peak
            calling runs consistently inside the apptainer container
          * Replace bioconda ``idr`` with pip install from ``sequana/idr``
            fork; fixes CI failures on Python 3.11/3.12 (upstream package
            is Python 3.10-only due to Cython 3.x incompatibility)
          * Fix ``plot_FRiP``: was iterating over all comparisons inside each
            rule invocation causing ``FileNotFoundError`` in parallel runs;
            now processes only its own wildcard
          * Fix IDR rules (``idr_NT``, ``self_pseudo_replicate_idr``,
            ``pseudo_replicate_idr``): IDR exits non-zero on sparse data;
            added ``|| true`` + conditional ``mv`` so the pipeline continues
            and downstream Python rules handle empty results gracefully
            peaks and Homer returns an empty DataFrame
          * Fix ``fastp`` rule: use ``input.fastq`` / ``output.r1`` /
            ``output.r2`` to match the sequana-wrappers fastp shell interface;
            split into paired/single-end branches
          * Add ``log:`` directives and stderr redirection to rules that were
            missing them: ``phantom_align``, ``chrom_sizes``, ``fingerprints``,
            ``bam_to_bed``, ``bed_to_bigwig``, ``pseudo_replicate_idr``
          * Update ``sequana_tools`` container to ``26.1.14``
          * Update CI: Python 3.10/3.11/3.12; ``actions/checkout@v4``
0.11.0    * Switch to click and new sequana_pipetools
0.10.0    * Fix design in case of samples that start with the same prefix
          * Include final IDR plots and tables
          * Fix containers and wrappers in the config file
          * Better HTML report
0.9.1     * Fix requirements and setup.py (remove wrong idr package)
0.9.0     * Use latest wrappers and apptainer (for rulegraph)
0.8.0     **First release.**
========= ====================================================================


Contribute & Code of Conduct
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To contribute to this project, please take a look at the
`Contributing Guidelines <https://github.com/sequana/sequana/blob/main/CONTRIBUTING.rst>`_ first. Please note that this project is released with a
`Code of Conduct <https://github.com/sequana/sequana/blob/main/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.
