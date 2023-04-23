# getNLR-pairs README

The getNLR-pairs pipeline is a rapid, user-friendly, and precise method to detect NLR-pairs in plant genomes.

## Prerequisites

### [Mamba](https://github.com/mamba-org/mamba)

We recommend utilizing [mamba](https://github.com/conda-forge/miniforge#mambaforge)for the installation and management of the necessary software. Execute the following code to install Mamba:

````sh
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
bash Mambaforge-Linux-x86_64.sh

# Create a conda environment
mamba create --name nlrpairs
````

### R and tidyverse

````sh
mamba install -c conda-forge r-base
mamba install -c conda-forge r-tidyverse
````

### [HMMER](http://hmmer.org/)

HMMER is used to pridict the NB-ARC domain.

```sh
mamba install -c bioconda hmmer
```

### [NLR-Annotator](https://github.com/steuernb/NLR-Annotator)

NLR-Annotator is a tool to annotate loci associated with NLRs.

```sh
git clone https://github.com/steuernb/NLR-Annotator.git
```

## Installation

Just download our repository getNLR-pairs.

````sh
git clone https://github.com/lixiang117423/getNLR-pairs.git
````

## Running

### Parse gene and mRNA information from GFF file

Given that a single gene may exhibit multiple transcript variants, our initial step was to extract the positional information of each transcript variant from the GFF file. This information included the respective ID, chromosome, start and end positions, as well as the strands.

````sh
python getGeneLocation.py -g test.gff -o gene.info.txt   
````

````sh
gene.id Chr     gene.start      gene.end        gene.strand     mRNA.id mRNA.start      mRNA.end
gene:Os01g0100100       1_wrky.20       2983    10815   +       transcript:Os01t0100100-01      2983    10815
gene:Os01g0100200       1_wrky.20       11218   12435   +       transcript:Os01t0100200-01      11218   12435
gene:Os01g0100300       1_wrky.20       11372   12284   -       transcript:Os01t0100300-00      11372   12284
gene:Os01g0100400       1_wrky.20       12721   15685   +       transcript:Os01t0100400-01      12721   15685
gene:Os01g0100466       1_wrky.20       12808   13978   -       transcript:Os01t0100466-00      12808   13978
gene:Os01g0100500       1_wrky.20       16399   20144   +       transcript:Os01t0100500-01      16399   20144
gene:Os01g0100600       1_wrky.20       22841   26892   +       transcript:Os01t0100600-01      22841   26892
gene:Os01g0100650       1_wrky.20       25861   26424   -       transcript:Os01t0100650-00      25861   26424
gene:Os01g0100700       1_wrky.20       27143   28644   +       transcript:Os01t0100700-01      27143   28644
````

### Predict NB-ARC domain using HMMER

```sh
hmmsearch --cpu 2 --domtblout hmmsearch.res.txt --cut_tc PF00931.hmm test.pep 
```

Extract protein sequence IDs and remove duplicate IDs.

````sh
sed '/^#/d' hmmsearch.res.txt | awk {'print $1'} | uniq > unique.hmmsearch.id.txt
````

### Annotate all CDS using [NLR-Annotator](https://github.com/steuernb/NLR-Annotator)

Upon performing a comparative analysis, we observed that including the entire genome coding sequence (CDS) as input in NLR-Annotator generated a greater number of NLRs. Therefore, we suggest employing the complete genome CDS to identify NLRs subsequent to HMMER analysis. We then recommend combining the outputs of both methods for the final results.

```sh
java -jar ~/NLR-Annotator/NLR-Annotator-v2.1b.jar -x ~/NLR-Annotator/src/mot.txt -y ~/NLR-Annotator/src/store.txt -i test.cds -g nlr.annotator.all.cds.res.txt -t 50

sed '/^#/d' nlr.annotator.all.cds.res.txt | awk {'print $1'} | uniq > nlr.annotator.all.cds.res.id.txt 
```



### Annotate NLR loci  of the two methods' results

Loci annotation of NB-ARC domain predicted by HMMER with [NLR-Annotator](https://github.com/steuernb/NLR-Annotator).

````sh
# merge all IDs
cat unique.hmmsearch.id.txt nlr.annotator.all.cds.res.id.txt | uniq > all.candidate.id.txt

# extract CDS
python getseq.py -i all.candidate.id.txt -f test.cds -o all.candidate.cds.fa

# run NLR-Annotator
java -jar ~/NLR-Annotator/NLR-Annotator-v2.1b.jar -x ~/NLR-Annotator/src/mot.txt -y ~/NLR-Annotator/src/store.txt -i all.candidate.cds.fa -g nlr.annotator.res.gff -t 10

# parse unique ID
sed '/^#/d' nlr.annotator.res.gff | awk {'print $1'} | uniq > nlr.annotator.res.id.txt       
````

### getNLRpairs

```sh
Rscript getNLRpairs.R gene.info.txt all.candidate.id.txt nlr.pairs.txt
```













