#!/usr/bin/env python3

# this program takes in input the file combined with all the AF informations, the FASTA file of all the
# proteins in the human proteome and the list of all the PTMs returning a file with a fixed header
# and a line for each residue in the format "Apos std_res AF_res AF_conf AF_sec_struct AF_contacts list_of_AF_contacts list_of_PTMs"

import sys
import itertools
import os
name_file1=sys.argv[1]
an=name_file1.split("/")[-1].split("_")[0]
file=open(sys.argv[2], "r")
sequence=""
start=False
for line in file:
    if (">" in line) and ((line.split("|")[1])==an):
        start=True
    elif (">" in line) and ((line.split("|")[1])!=an) and start:
        break
    elif (">" not in line) and start:
        sequence=sequence+line.split("\n")[0]
    else:
        continue
file.close()
file=open(sys.argv[3], "r")
PTMs=list(itertools.repeat("", 50000))
start=False
for line in file:
    if line.split(" ")[0]==an:
        start=True
        PTMs[int(line.split(" ")[1])-1]=PTMs[int(line.split(" ")[1])-1]+" "+line.split(" ")[3].split("\n")[0]+"-"+line.split(" ")[2]
    elif line.split("|")[0]!=an and start:
        break
    else:
        continue
file.close()
file1=open(name_file1, "r")
lines=file1.readlines()
file1.close()
ceck_length_sequence=True
name_file2=sys.argv[4]
if len(lines)==len(sequence):
    file2=open(name_file2, "w")
    file2.write("UniProt AN: "+an+"\n\n# position\n    # Uniprot reference proteome residue\n        # AlphaFold residue\n            # AlphaFold confidence value\n                # AlphaFold predicted secondari structure\n                    # AlphaFold predicted number of interacting residues (r = 8A)\n                        # list of annotated Phosphosite PTMs\n\n")
    for i in range (0, len(lines)):
        file2.write(lines[i].split(" ")[0]+"  "+sequence[i]+"  "+lines[i].split(" ")[1]+"  "+lines[i].split(" ")[2]+"  "+lines[i].split(" ")[3]+"  "+lines[i].split(" ")[4]+"  ["+lines[i].split("[")[1].split("]")[0]+"]  ["+PTMs[i]+" ]\n")
    file2.close()
else:
    os.remove(name_file2)
    file3=open(sys.argv[5], "a")
    file3.write(an+" has an unapdated AlphaFold primary sequence!\n")
    file3.close()