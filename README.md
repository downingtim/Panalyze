![Nextflow](https://img.shields.io/badge/nextflow-20.07.1-brightgreen)

![Docker](https://img.shields.io/badge/uses-docker-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-gray)
![Publication](https://img.shields.io/badge/Publication-OUP%20Bioinformatics-purple)

# Overview

Panalyze can make and analyse [pangenome variation graphs (PVGs)](https://doi.org/10.1093/bioinformatics/btac743). This was mainly designed with virus genomes in mind. It takes in a FASTA file of related sequences and constructs a PVG from them using [PGGB](https://github.com/pangenome/pggb). It visualises the PVG using [VG](https://github.com/vgteam/vg) and [ODGI](https://github.com/pangenome/odgi), and summarises it numerically using [GFAtools](https://github.com/lh3/gfatools) and ODGI. It calculates PVG openness using [Panacus](https://github.com/marschall-lab/panacus), [Pangrowth](https://peercommunityjournal.org/item/10.24072/pcjournal.415.pdf) and ODGI's heaps function. It gets the sample genome sizes and allocates them into communities (ie, groups) based on similarity. It identifies mutations in the form of VCFs using GFAutil and gets presence-absence variants (PAVs). It has a range of optional functions, like downloading a query to create the input FASTA, and using the [BUSCO database](https://busco.ezlab.org/) to quantify the numbers of genes in the samples of interest.

You can read our preprint [here](https://www.biorxiv.org/content/10.1101/2025.04.10.646565) and some ideas behind this [here](https://arxiv.org/abs/2412.05096). Panalyze works in a [Docker](https://www.docker.com/resources/what-container) container and runs in [NextFlow](https://www.nextflow.io/).

## Installation

Clone the directory

    git clone https://github.com/downingtim/Panalyze/

Go to the folder

    cd Panalyze

Run in Nextflow given a template YML file and an example FASTA file. You may need to activate docker and R to ensure it works smoothly. You need Java version 11+ as well.

For example, we can examine a small set of goatpox virus (GTPV) genomes:

    nextflow run main.nf --config template.GTPV.yml --reference test_genomes.GTPV.fa

Note that for your own samples, you will need to remove special characters in your sample names. In addition, to ensure compatibility with other pangenome graph tools, please adhere to the [PanSN-spec: Pangenome Sequence Naming](https://github.com/pangenome/PanSN-spec) guidance, which basically means adding a hash and a digit onto the end of the sample names.


## Examples ## 

In another example, we can examine a set of 142 foot-and-mouth virus (FMDV) serotype A genomes:

    nextflow run main.nf --config template.FMDV.A.yml --reference test_genomes.FMDV.A.fa

We can examine a set of 441 foot-and-mouth virus (FMDV) serotype O genomes:

    nextflow run ../main.nf --config template.FMDV.O.yml --reference test_genomes.FMDV.O.fa

We can examine a set of 18 foot-and-mouth virus (FMDV) serotype C genomes:

    nextflow run ../main.nf --config template.FMDV.C.yml --reference  test_genomes.FMDV.C.fa

We can take 121 lumpy skin disease virus (LSDV) genomes:

    nextflow run main.nf --config template.LSDV.yml --reference test_genomes.LSDV.fa

We can take 31 sheeppoxvirus (SPPV) genomes:

    nextflow run main.nf --config template.SPPV.yml --reference test_genomes.SPPV.fa  

We can take 132 lumpy skin disease virus (LSDV) genomes but just 7.5 Kb spanning 2.5-10 Kb of their aligned genomes:

    nextflow run main.nf --config template.LSDV.10kb.yml --reference test_genomes.LSDV.10kb.fa

We can take 132 lumpy skin disease virus (LSDV) genomes but just 5 Kb spanning 135-140 Kb of their aligned genomes:

    nextflow run main.nf --config template.LSDV.135kb.yml --reference test_genomes.LSDV.135kb.fa

We can run on a large DNA test dataset - 13 GTPV genomes (at the time of writing) to be downloaded based on the text in the template file:

    nextflow run main.nf --config template.GTPV.all.yml 

We can run on a ssRNA test dataset - 15 porcine respiratory coronavirus genomes to be downloaded:

    nextflow run main.nf --config template.PRCV.all.yml

We can investigate 2,358 mpox genomes:

    nextflow run main.nf --config template.MPOX.yml --reference test_genomes.mpox.fa

We can investigate 414 Rift Valley fever virus (RVFV) S segment sequences:

    nextflow run main.nf --config template.RVFV.S.yml --reference test_genomes.S.fa

We can investigate 302 Rift Valley fever virus (RVFV) M segment sequences:

    nextflow run main.nf --config template.RVFV.M.yml --reference test_genomes.M.fa 

We can investigate 306 Rift Valley fever virus (RVFV) L segment sequences:

    nextflow run main.nf --config template.RVFV.L.yml  --reference test_genomes.L.fa


## Module selection

By default, the modules will be active if the associated component in the 'MODULES' is 'on' (has a digit 1 following its entry) in the template YML file. To turn a module 'off', put 0 after the module in the template YML file.


## Speeding it up

You can skip some modules: the HEAPS_Visualize module takes a considerable amount of time. Toggle these using the template file.  


## Java issue

In the event that you have a Java version issue, you should ensure you have version 11 or higher and the commands below may assist (you may need to edit these):

    export JAVA_HOME=/cm/shared/apps/mambaforge/envs/tools
    export PATH=$JAVA_HOME/bin:$PATH



## Make your own run

In your own template YML file, you will need to define the dataset name, number of haplotypes, max number of CPUs available, minimum expected genome size, sample name filtering if using the download function, and the BUSCO clade (if relevant).

## How does it work?

The input data is "test_genomes.GTPV.fa" in this example. You can switch this to your own FASTA file input: in main.nf, Panalyze has a Download module which is not active by default.
vvvvThe modules folder contains the processes, which are called by main.nf. These may call tools and scripts in other folders like bin.


## Main components:
### [1]  DOWNLOAD: (optional)
     [i]   Download all 'complete genomes' or 'genomic sequences' from Nucleotide matching your text query of a specific defined organism (using the [orgn] search condition).
### [2]  ALIGN: (optional)
     [i]  Align the genomes with MAFFT -> see results/align/
     [ii] Construct a phylogeny with RAxML using a GTR+G4 substitution model -> see results/align/
### [3]  TREE: (optional)
     [i]   Visualise the phylogeny with R -> tree.png
### [4]  MAKE_PVG: (core)
     [i]   Construct a PVG using PGGB based on a 90% identity threshold and a match length of 1 Kb -> results/PVG/pggb.gfa
### [5]  VIZ1: (core)
     [i]   Create a PVG visualisation PNG with VG's view function and dot -> results/vg/out.vg.png - note this file size is very large and may take time to resolve on any visualisation tool
### [6]  ODGI: (core)
     [i]   Create OG file with odgi -> results/odgi/out.og
     [ii]  Extract odgi PVG metrics from OG file -> results/odgi/odgi.stats.txt
### [7]  OPENNESS_PANACUS: (core)
     [i]   Get the number of haplotypes present (usually equal to the number of genomes) -> results/panacus/haplotypes.txt
     [ii]  Run Panacus to get the rates of PVG growth as more samples are added -> results/panacus/histgrowth.node.tsv
     [iii] Visualise the PVG growth -> results/panacus/histgrowth.node.pdf
### [8]  OPENNESS_PANGROWTH: (core)
     [i]   Make a folder SEQS and split the genomes into individual files inside it.
     [ii]  Add the genomes to a fastix shared file and run pangrowth 
     [iii] Plot the allele frequency spectrum (AFS) -> results/pangrowth/pangrowth.pdf
     [iv]  Plot the PVG growth -> results/pangrowth/growth.pdf
     [v]   Plot the PVG core size -> results/pangrowth/p_core.pdf
### [9]  PATH_FROM_GFA: (core)
     [i]   Get the sample names from the PVG
### [10] VCF_FROM_GFA: (core)
     [i]   Use gfautil to convert the GFA to VCF -> results/vcf/gfavariants.vcf
### [11] VCF_PROCESS: (core)
     [i]   Use gfautil and Bash to quantify the pairwise difference in genome coordinates across samples.
     [ii]  Visualise this using R -> results/vcf/variation_map-basic.pdf
     [iii] Get the SNP density across the genomes -> results/vcf/mutation_density.pdf
     [iv]  Count the AFS based on this SNP data -> out file
### [12] GETBASES: (core)
     [i]   Generate a BED file based on the odgi file -> result/out.bed
     [ii]  Get the sequence length per genome
### [13] VIZ2: (core)
     [i]   Create large-scale PVG visualisation using Odgi's viz function -> result/out.viz.png
### [14] HEAPS: (core)
     [i]   Run Odgi's heaps function across all samples to get rate of PVG growth -> results/heaps/heaps.txt
### [15] HEAPS_Visualize: (core)
     [i]   Visualise the output from Odgi's heaps function in HEAPS -> results/heaps/heaps.pdf
### [16] PAVS: (core)
     [i]   Use Odgi to get presence-absence variants (PAVs) (a large file!)
     [ii]  Quantify the number of PAVs -> result/out.flatten.fa
### [17] PAVS_plot: (core)
     [i]   Visualise the PAVs from PAVS -> result/pavs/out.flatten.pavs.pdf
### [18] COMMUNITIES: (core)
     [i]   Use wfmash to quantify the number of communities based on a 90% similarity threshold and at least 6 mappings per segment.
     [ii]  Convert these mapping into a network that is visualised -> genomes.mapping.paf
### [19] PAFGNOSTIC: (core)
     [i]   Create a text file of the mapping from the COMMUNITIES -> pafgnostic.txt
### [20] GFAstat: (core)
    [i]    Compute key PVG metrics with GFAstats  -> results/gfastat/gfa.stats.txt
    [ii]   Get the genome lengths -> results/gfastat/genome.lengths.txt
### [20] Annotate_Position: (core)
    [i]    Use ODGI to map PVG nodes to annotation data
    [ii]   Provide instructions on using Bandage
### [22] BUSCO: (optional)
     [i]   Use Busco to count the number of BUSCO genes present.

## Dependencies

Panalyze is based on the following tools and scripts. If you use the Docker version, this should not be an issue.

1.  Esearch cand efetch
2.  Mafft
3.  RAxML
4.  R
5.  VG
6.  dot
7.  PGGB
8.  ODGI
9.  Panacus
10. Pangrowth
11. Gfautil
12. Wfmash
13. Pafgnostic
14. GFAstats
15. Busco
16. Bgzip
17. SAMtools
18. Mash
19. Gffread
20. Prokka

## Credits

Tim Downing, Chandana Tennakoon, Thibaut Freville

## MIT License

Copyright (c) [2025] [Panalyze] 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
