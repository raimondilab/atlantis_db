#!/usr/bin/env python3

import sys
import os
pdb_list=[]
found=True
still=False
pdb_code=sys.argv[1]
file1=open(sys.argv[2], "r")
for line in file1:
    if pdb_code in line:
        found=False
        break
file1.close()
if found:
    os._exit(1)
file2=open(sys.argv[3], "r")
for line in file2:
    if line[0:4]==pdb_code:
        still=True
        found=True
    else:
        still=False
    if found and not still:
        break
    if found and still:
        chain=line.split("\t")[0]+"_"+line.split("\t")[1]
        if chain not in pdb_list:
            pdb_list.append(chain)
file2.close()
file3=open(sys.argv[4], "w")
for element in pdb_list:
    file3.write(element+"\n")
file3.close()
sys.exit(2)