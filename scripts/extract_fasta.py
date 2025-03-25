#!/usr/bin/env python3

import sys
import os
file1=open(sys.argv[1], "r")
folder=sys.argv[2]
name_file_unuseful=folder+"/unuseful_file.txt"
file2=open(name_file_unuseful, "w")
for line in file1:
    if line[0]==">":
        file2.close()
        name_file=folder+"/"+line.split("|")[1]+"_seq.fasta"
        file2=open(name_file, "w")
        print(name_file)
        file2.write(line)
    else:
        file2.write(line)
file2.close()
file1.close()
os.remove(name_file_unuseful)