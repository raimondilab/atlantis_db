#!/usr/bin/env python3

# this program takes in input one file at the time and cecks if there is one file "complete" for that protein:
# if it exists, the information are added, oterwise the file is created
# the "complete" has no header and contains a list of all the residue in the protein in the form:
# "Aposition max_number_of_contacts_in_a_single_structure_of_that_protein [ list_of_the_residues_interacting_in_at_least_one_structure_divided_by_one_space ]"

def Union(lst1, lst2):
    final_list=list(set(lst1) | set(lst2))
    final_list.sort()
    return final_list

import sys
import itertools
list_an=[]
file=open(sys.argv[2], "r")
for line in file:
    an=line.split("\n")[0]
    list_an.append(an)
file.close()
name_file_input=sys.argv[1]
name=name_file_input.split("AF_")[1]
an=name.split("_")[0]
if an not in list_an:
    exit()
file1=open(name_file_input, "r")
number=int(name.split("_")[1])
cut="_"+name.split("_")[1]+"_"
if number==1:
    name_file_output=name_file_input.split(cut)[0]+"_complete_AF_contacts.txt"
    file2=open(name_file_output, "a")
    for line in file1:
        if line!="\n":
            row=line.split("\n")[0]
            file2.write(row.split(" [")[0]+" "+row.split("]  ")[1]+" ["+row.split("[")[1].split("]")[0]+"]\n")
    file2.close()
else:
    name_file_output=name_file_input.split(cut)[0]+"_complete_AF_contacts.txt"
    file2=open(name_file_output, "r")
    f2=list(itertools.repeat("", 50000))
    f2n=list(itertools.repeat(0, 50000))
    i=0
    for line in file2:
        if line!="\n":
            row=line.split("]")[0]
            f2[i]=row.split("[ ")[1]
            row=line.split(" [")[0]
            f2n[i]=int(row.split(" ")[1])
            i=i+1
    file2.close()
    file2=open(name_file_output, "w")
    for i in range (0, (200*(number-1))):
        file2.write("A"+str(i+1)+" "+str(f2n[i])+" [ "+f2[i]+"]\n")
    i=0
    for line in file1:
        row=line.split("\n")[0]
        if int(row.split("] ")[1])>f2n[i+(200*(number-1))]:
            file2.write("A"+str(i+(200*(number-1))+1)+" "+row.split("]  ")[1])
        else:
            file2.write("A"+str(i+(200*(number-1))+1)+" "+str(f2n[i+(200*(number-1))]))
        if (f2[i+(200*(number-1))]==""):
            file2.write(" ["+line.split("[", 1)[1].split("]")[0]+"]\n")
        elif ((line.split("[", 1)[1].split("]")[0])==" "):
            file2.write(" [ "+f2[i+(200*(number-1))]+"]\n")
        else:
            row=f2[i+(200*(number-1))]+"]"
            r1=row.split(" ]")[0]
            row=line.split(" ]")[0]
            r2=row.split("[")[1]
            if (r2!=""):
                r2=r2.split(" ", 1)[1]
            list_old=r1.split(" ")
            list_new=r2.split(" ")
            united=Union(list_old, list_new)
            file2.write(" [ ")
            for element in united:
                file2.write(element+" ")
            file2.write("]\n")
        i=i+1
    file2.close()
file1.close()