#!/usr/bin/env python3

import sys
import itertools

name=sys.argv[1]
f=name.split("/contacts/")[1]
an=f.split("_pdb_")[0]
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
lines=list(itertools.repeat("", 100000))
file=open(name, "r")
i=0
for line in file:
    if line!="\n":
        lines[i]=line
        i=i+1
file.close()
file=open(name, "w")
file.write("UniProt AN:  "+an+";\n\n")
for i in range(0, len(sequence)):
    if " " in lines[i]:
        file.write(an+"_"+str(i+1)+" "+sequence[i]+" "+lines[i].split(" ", 1)[1])
    else:
        file.write(an+"_"+str(i+1)+" "+sequence[i]+"\n")
file.close()