# enzyme-mining-aox
An enzyme mining process based on python and multiple bioinformatics tools and exemplifies its application to methanol oxidase (AOX).

This is the online repository for the submitted paper "".

## Installation

### python environment

```python
conda create -n enzyme_mining python=3.8
conda activate enzyme_mining
conda install pandas
conda install ipykernel
pip install pymed
conda install biopython
conda install scipy
conda install scikit-learn
```

### Bioinformatic tools

| Software    | Version                    | URL                                                          |
| ----------- | -------------------------- | ------------------------------------------------------------ |
| CD-HIT      | 4.8.1                      | https://github.com/weizhongli/cdhit/releases (linux)         |
| T-Coffee    | 11.00                      | https://tcoffee.org/Projects/tcoffee/index.html (linux)<br />https://tcoffee.crg.eu/ (online) |
| HMMER       | 3.3 <br />(2.41.2, online) | http://hmmer.org/ (linux)<br />https://www.ebi.ac.uk/Tools/hmmer/search/phmmer (online) |
| SWISS-MODEL | 2023.11.04                 | https://swissmodel.expasy.org/                               |
| USEARCH     | 11.0.667                   | http://www.drive5.com/usearch/ (linux, windows)              |
| TM-align    | 20190822                   | https://zhanggroup.org/TM-align/ (linux)                     |

The repository contains the necessary intermediate files needed to reproduce the results, for development it is recommended to use the latest stable version of the softwares and online services.

### Visualization tools

| Software  | Version  | URL                            |
| --------- | -------- | ------------------------------ |
| Jalview   | 2.11.2.7 | https://www.jalview.org/       |
| Cytoscape | 3.9.1    | https://cytoscape.org/         |
| iTOL      | -        | https://itol.embl.de/ (online) |



### Online databases

| Database      | URL                                    |
| ------------- | -------------------------------------- |
| BRENDA        | https://www.brenda-enzymes.org/        |
| UniProt       | https://www.uniprot.org/               |
| NCBI          | https://www.ncbi.nlm.nih.gov/protein   |
| NCBI Taxonomy | https://ftp.ncbi.nih.gov/pub/taxonomy/ |



## Steps

### Download data

Get the corresponding list page from the Brenda's EC page and UniProt search page. Save the results to the files. For alcohol oxidase (EC 1.1.3.13), the pages are:

https://www.brenda-enzymes.org/enzyme.php?ecno=1.1.3.13

https://www.uniprot.org/uniprotkb?query=(ec:1.1.3.13)%20NOT%20(ec:1.1.3.20)

The focus here is on sequence, literature and organisms.

| Database | Content                                                    |
| -------- | ---------------------------------------------------------- |
| Brenda   | sequence(Uniprot ID), organism(name), Reference(PubMed ID) |
| UniProt  | Entry, Reviewed, Organism, Sequence, PubMed ID             |
| PubMed   |                                                            |

UniProt database as a primary source of sequence data.









2. 