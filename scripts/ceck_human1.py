#!/usr/bin/env python3

import sys
pdbs=[]
chains=[]
file1=open(sys.argv[3], "r")
file_pdb=open(sys.argv[1], "w")
file_chains=open(sys.argv[2], "w")
print("started")
for line in file1:
    if "9606" in line:
        pdb=line.split("\t")[0]
        chain=line.split("\t")[0]+"_"+line.split("\t")[1]
        if pdb not in pdbs:
            pdbs.append(pdb)
            print(pdb, file=file_pdb, flush=True)
        if chain not in chains:
            chains.append(chain)
            print(line.split("\n")[0], file=file_chains, flush=True)
file1.close()
file_chains.close()
file_pdb.close()