#!/usr/bin/env python3

# this program takes as imput the file containing the FASTAs af all the proteins in the human proteome and
# returns a file containing the list ao all the accession numbers, one per line with non header or any other
# character per line

import sys
list=[]
file=open(sys.argv[1], "r")
for line in file:
    if ">" in line:
        an=line.split("|")[1]
        list.append(an)
file.close()
list.sort()
file=open(sys.argv[2], "w")
for element in list:
    file.write(element+"\n")
file.close()