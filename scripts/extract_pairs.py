#!/usr/bin/env python3

import sys
import os
proteome=[]
file=open(sys.argv[3], "r")
for line in file:
    proteome.append(line.split("\n")[0])
file.close()
file1=open(sys.argv[1], "r")
folder=sys.argv[2]
protein="PPP"
domain="DDD"
change=False
ceck_proteome=False
name_file_unuseful=folder+"/unuseful_file.txt"
file2=open(name_file_unuseful, "w")
next(file1)
next(file1)
next(file1)
for line in file1:
    if line.split("\t")[0]!=protein:
        protein=line.split("\t")[0]
        change=True
        if protein in proteome:
            ceck_proteome=True
        else:
            ceck_proteome=False
    if line.split("\t")[5]!=domain:
        domain=line.split("\t")[5]
        change=True
    if change and ceck_proteome:
        file2.close()
        name_file=folder+"/"+line.split("\t")[0]+"_"+line.split("\t")[5]+".txt"
        file2=open(name_file, "w")
        print(name_file)
        file2.write(str(int(line.split("\t")[3])-5)+"   "+str(int(line.split("\t")[4])+5)+"\n")
        change=False
    elif ceck_proteome:
        file2.write(str(int(line.split("\t")[3])-5)+"   "+str(int(line.split("\t")[4])+5)+"\n")
    else:
        continue
file2.close()
file1.close()
os.remove(name_file_unuseful)