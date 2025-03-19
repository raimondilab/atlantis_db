An integrative daTabase for human proteome structuraL And FuNcTIonal Sites

Welcome to the Atlantis Complementary Repository!

Understanding the functional role of specific residues is crucial for deciphering protein function, regulation, and interaction networks. To this endeavor, we have created the Atlantis database, which provides an extensive resource for understanding the role of specific residues in protein structures, complexes, and interaction networks. The database integrates various structural and functional annotation layers for each residue, offering a comprehensive understanding of protein functionality.

Atlantis annotates 11,378,289 residues across 20,594 human proteins. Additionally, it identifies 888,080 intra-protein contacts in 55,736 PDB structures and 786,063 inter-protein contacts in 11,320 PDB structures.

 
## Methods

We extracted a list of all the UniProt accession numbers from the file containing the FASTA sequence for the entire human proteome database. Next, we extracted and mapped each residue's structural and functional annotation layers. Following that, we calculated the contacts for each PDB and AF structure.

![](/frontend/public/assets/images/workflow.png)

## Architecture 

We developed a GraphQL API to provide direct open access to data. The API documentation page offers comprehensive information about the API's functionality and supported methods. Moreover, it enables quick and effortless data retrieval, making it easier to locate structural and functional annotations and facilitating integration in data analysis, machine learning pipelines, and more. 

![](/frontend/public/assets/images/graphql.png)

