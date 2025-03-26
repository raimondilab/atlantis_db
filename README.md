[![DOI](https://zenodo.org/badge/819387466.svg)](https://doi.org/10.5281/zenodo.15091436)

An integrative daTabase for human proteome structural And FuNcTIonal Sites

![](/logo.png)

Welcome to the Atlantis Complementary Repository!

Understanding the functional role of specific residues is crucial for deciphering protein function, regulation, and interaction networks. To this endeavor, we have created the Atlantis database, which provides an extensive resource for understanding the role of specific residues in protein structures, complexes, and interaction networks. The database integrates various structural and functional annotation layers for each residue, offering a comprehensive understanding of protein functionality.

Atlantis annotates 11,378,289 residues across 20,594 human proteins. Additionally, it identifies 888,080 intra-protein contacts in 55,736 PDB structures and 786,063 inter-protein contacts in 11,320 PDB structures.

Explore ![Atlantis]("https://atlantis.bioinfolab.sns.it").
 
## Methods

We extracted a list of all the UniProt accession numbers from the file containing the FASTA sequence for the entire human proteome database. Next, we extracted and mapped each residue's structural and functional annotation layers. Following that, we calculated the contacts for each PDB and AF structure.

![](/workflow.png)


## Structure of this Repository

There are two main folders:

1. '/data' -  contains the datasets, necessary input, and output files categorized into different subfolders.
2. '/scripts' - contains the codes used to develop Atlantis.

## Output page of the web application
#### Functional site information section
This section provides various types of annotations at the residue level, including UniProt annotations such as variants, molecule processing, membrane localization, motifs, domains, glycosylations, lipidations, modified residues, disulfide bonds, and secondary structures. Protein architecture information is provided through PFAM and InterPro domains and aligned positions in the Hidden Markov Model (HMM). Additionally, it includes information on IntAct binding regions and protein post-translational modifications sourced from PhosphoSitePlus.

![Coupling probabilities table](static/img/GIFs/couplingProbabilities.gif)
