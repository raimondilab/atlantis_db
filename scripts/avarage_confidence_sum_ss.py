#!/usr/bin/env python3

# this program takes in nput a confidence and the corresponding contacts file and unites the in the form:
# "Aposition residue avarage_confidence consensus_secondary_structure max_number_of_contacts [ list_of_all_contacts ]"

import sys
import itertools
name_file_confidence=sys.argv[1]
name_file_contacts=sys.argv[2]
name_file_output=sys.argv[3]
confidence=list(itertools.repeat("unk", 100000))
contacts=list(itertools.repeat("0 [ ]\n", 100000))
file1=open(name_file_confidence, "r")
i=1
for line in file1:
    value=(float(line.split(" ")[2]))/(int(line.split(" ")[3]))
    value="{:.2f}".format(value)
    confidence[i]=(line.split(" ")[0]+" "+line.split(" ")[1]+" "+str(value)+" "+line.split(" ")[4].split("\n")[0])
    i=i+1
file1.close()
lenght=i
file2=open(name_file_contacts, "r")
i=1
for line in file2:
    contacts[i]=line.split(" ", 1)[1]
    i=i+1
file2.close()
file3=open(name_file_output, "w")
for l in range (1, lenght):
    file3.write(confidence[l]+" "+contacts[l])
file3.close()
