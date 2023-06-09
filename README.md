# getNLR-pairs README

The getNLR-pairs pipeline is a rapid, user-friendly, and precise method to detect NLR-pairs in plant genomes.

## Prerequisites

### [Mamba](https://github.com/mamba-org/mamba)

We recommend utilizing [mamba](https://github.com/conda-forge/miniforge#mambaforge) for the installation and management of the necessary software. Type the following code to install Mamba:

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

NLR-Annotator is a tool to annotate loci associated with NLRs. **Note: NLR-Annotator needs to be in the same folder as the project.**

```sh
git clone https://github.com/steuernb/NLR-Annotator.git
```

## Installation

Just clone our thie repository :

````sh
git clone https://github.com/lixiang117423/getNLR-pairs.git
````

## Running

### Preparing example data

We used the wheat, maize and rice genomes from the [Ensembl Plants](https://plants.ensembl.org/index.html)database repository as example data.

````sh
# create folder
mkdir example

# doanload the example data
wget https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-56/fasta/triticum_aestivum/dna/Triticum_aestivum.IWGSC.dna.toplevel.fa.gz -O ./example/wheat.fa.gz
wget https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-56/gff3/triticum_aestivum/Triticum_aestivum.IWGSC.56.gff3.gz -O ./example/wheat.gff.gz

wget https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-56/fasta/zea_mays/dna/Zea_mays.Zm-B73-REFERENCE-NAM-5.0.dna.toplevel.fa.gz -O ./example/maize.fa.gz
wget https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-56/gff3/zea_mays/Zea_mays.Zm-B73-REFERENCE-NAM-5.0.56.gff3.gz -O ./example/maize.gff.gz

wget https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-56/fasta/oryza_sativa/dna/Oryza_sativa.IRGSP-1.0.dna.toplevel.fa.gz -O ./example/rice.fa.gz
wget https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-56/gff3/oryza_sativa/Oryza_sativa.IRGSP-1.0.56.gff3.gz -O ./example/rice.gff.gz

# Decompress all files
gunzip ./example/*.gz
````

### Preparing  sample list

Enter the prefixes of the above files into sample.list, e.g:

````
vi sample.list.example

rice
maize
wheat
````

### Run getNLRpairs

````sh
python3 run.getNLR-pairs.py -i example -s sample.list.example -o result
````

Meaning of each parameter:

- i: Folder containing genome and annotation files.
- s: sample.list.
- -o: This is the folder where temporary files are stored and will be deleted when the program is finished.

When the run is complete, a result file is generated in the current directory, such as `wheat.nlr.pairs.txt`:

```
gene.1  gene.2  chr.1   chr.2   start.1 start.2 end.1   end.2   strand.1        strand.2
gene:TraesCSU02G244700  gene:TraesCSU02G244800  Un_328  Un_328  367843085       367883403       367844098       367884368       +       -
gene:TraesCSU02G232800  gene:TraesCSU02G232900  Un_328  Un_328  344888847       345034816       344890891       345035865       +       +
gene:TraesCSU02G224800  gene:TraesCSU02G225000  Un_328  Un_328  331470513       331543914       331471370       331545378       -       +
gene:TraesCSU02G205200  gene:TraesCSU02G205300  Un_328  Un_328  305404604       305533325       305407847       305534248       +       -
gene:TraesCSU02G203600  gene:TraesCSU02G203800  Un_328  Un_328  303068051       303377185       303070317       303378502       -       +
gene:TraesCSU02G196500  gene:TraesCSU02G196800  Un_328  Un_328  294162942       294373659       294166815       294375605       +       +
gene:TraesCSU02G171700  gene:TraesCSU02G172000  Un_328  Un_328  253065268       253482556       253071297       253488689       -       +
gene:TraesCSU02G168100  gene:TraesCSU02G168400  Un_328  Un_328  246505692       247570454       246508354       247574434       +       -
gene:TraesCSU02G135400  gene:TraesCSU02G135500  Un_328  Un_328  117147569       117293768       117152623       117300952       +       -
```

## Contact

Xiang LI: lixiang117423@gmail.com
