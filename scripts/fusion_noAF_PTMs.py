#!/usr/bin/env python3

import sys
import itertools
import os.path
list_human=[]
file=open(sys.argv[1], "r")
for line in file:
    list_human.append(line.split("\n")[0])
file.close()
workdir_AF=sys.argv[2]
for an in list_human:
    name_file=workdir_AF+an+"_complete_residues_AF_PTMs.txt"
    if not os.path.exists(name_file):
        file=open(sys.argv[3], "r")
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
        file=open(sys.argv[4], "r")
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
        file1=open(name_file, "w")
        file1.write("UniProt AN: "+an+"\n\n# position\n    # Uniprot reference proteome residue\n        # AlphaFold residue\n            # AlphaFold confidence value\n                # AlphaFold predicted secondari structure\n                    # AlphaFold predicted number of interacting residues (r = 8A)\n                        # list of annotated Phosphosite PTMs\n\n")
        for i in range (0, len(sequence)):
            file1.write("A"+str(i+1)+"  "+sequence[i]+"  none  none  none  none  [ unk ]  ["+PTMs[i]+" ]\n")
        file1.close()