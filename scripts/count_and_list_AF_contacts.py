#/usr/bin/env python3

# this program takes in input a file containing all the contacts inside an AF structures and retursn a file
# with no header that contains a list of all the residue in the protein the the form:
# "Aposition number_of_contacts [ list_of_the_interacting_residues_divided_by_one_space ]"

import sys
name_file_input=sys.argv[1]
file1=open(name_file_input, "r")
x=name_file_input.split("AF_")[1]
an=x.split("-F")[0]
n=x.split("-F")[1]
number=int(n.split("-model")[0])
if number<=9:
    name_file_output=name_file_input.split("AF_")[0]+"AF_"+an+"_00"+str(number)+"_3dc_list.txt"
elif number<=99:
    name_file_output=name_file_input.split("AF_")[0]+"AF_"+an+"_0"+str(number)+"_3dc_list.txt"
else:
    name_file_output=name_file_input.split("AF_")[0]+"AF_"+an+"_"+str(number)+"_3dc_list.txt"
file2=open(name_file_output, "w")
protein=[]
interactors=[]
last_residue=0
for line in file1:
    if len(line.split(" "))==1:
        break
    res1=line.split(" ")[0]
    res2=line.split(" ")[1]
    interactors.append(res1.split("/")[1]+" "+res2.split("/")[1])
    for element in (line.split(" ")):
        residue=int(element.split("/")[1])
        if residue not in protein:
            protein.append(residue)
        if residue>last_residue:
            last_residue=residue
protein.sort()
for l in range (1, last_residue+1):
    file2.write("A"+str(l)+" [")
    count=0
    if l in protein:
        for element in interactors:
            if str(l)==(element.split(" ")[1]):
                file2.write(" "+str(int(element.split(" ")[0])+(200*(number-1))))
                count=count+1
        for element in interactors:
            if str(l)==(element.split(" ")[0]):
                file2.write(" "+str(int(element.split(" ")[1])+(200*(number-1))))
                count=count+1
    file2.write(" ]  "+str(count)+"\n")
file1.close()
file2.close()