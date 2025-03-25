#!/usr/bin/env python3

import os.path
import itertools
import sys
protein_list=[]
acc_list=[]
list_an=[]
file1=open(sys.argv[1], "r")
file2=open(sys.argv[2], "r")
id=True
acc=False
gn=False
for line in file2:
    if line=="//\n":
        next(file2)
        break
for line in file2:
    if id and line.split("   ")[0]=="ID":
        l1=line.split(".\n")[0]
        l2=l1.replace(";", " ")
        l3=l2.replace("       ", " ")
        l4=l3.replace("      ", " ")
        l5=l4.replace("     ", " ")
        l6=l5.replace("    ", " ")
        l7=l6.replace("   ", " ")
        l8=l7.replace("  ", " ")
        list_id=l8.split("ID ")[1]
        id=False
        acc=True
    if acc and line.split("   ")[0]=="AN":
        l1=line.split("\n")[0]
        list_acc=l1.split("ACCESSION: ")[1]
        acc=False
        gn=True
    if gn and line.split("   ")[0]=="GN":
        l1=line.split("\n")[0]
        list_gn=l1.split("   ")[1]
        gn=False
    if line=="//\n":
        if gn:
            list_gn="none"
            gn=False
        id=True
        acc_list.append(list_acc.split(";")[0])
        protein_list.append("UniProt AN:  "+list_acc+"\nUniProt ID:  "+list_id.split(" ")[0]+";\nGene Name:  "+list_gn+"\nLength:  "+list_id.split(" ")[2]+"aa;\nStatus:  "+list_id.split(" ")[1]+";")
acc_list.append(list_acc.split(";")[0])
protein_list.append("UniProt AN:  "+list_acc+"\nUniProt ID:  "+list_id.split(" ")[0]+";\nGene Name:  "+list_gn+"\nLength:  "+list_id.split(" ")[2]+"aa;\nStatus:  "+list_id.split(" ")[1]+";")
file2.close
for line in file1:
    an=line.split("\n")[0]
    list_an.append(an)
    if an not in acc_list:
        protein_list.append("UniProt AN:  "+an+";\nUniProt ID:  none;\nGene Name:  none;\nLength:  und;\nStatus:  unk;")
file1.close()
workdir=sys.argv[3]
for element in protein_list:
    ann=element.split(";")[0]
    an=ann.split("UniProt AN:  ")[1]
    lengthh=element.split("aa;\n")[0]
    name_file=workdir+an+"_complete_residues_AF_PTMs.txt"
    file3=open(name_file, "r")
    lines=file3.readlines()
    file3.close()
    count=0
    for line in lines:
        if line[0]=="A":
            count=count+1
    if "und" not in lengthh.split("Length:  ")[1]:
        length=int(lengthh.split("Length:  ")[1])
    else:
        length=count
    if count==length:
        file3=open(name_file, "w")
        file3.write(element+"\n\n")
        for line in lines:
            if line[0]!="A" and line[0]!="U":
                if "8" in line:
                    file3.write("                    # AlphaFold maximum predicted number of interacting residues in a single structure (r = 8A)\n                        # AlphaFold list of residue with a predicted interaction in at least one structure (r = 8A)\n")
                elif "PTMs" in line:
                    file3.write("    "+line)
                elif "secondari" in line:
                    file3.write("                # AlphaFold predicted secondary structure\n")
                else:
                    file3.write(line)
            elif line[0]!="U":
                file3.write(line)
        file3.close()
    else:
        os.remove(name_file)
        file4=open(sys.argv[4], "a")
        file4.write(an+" has incoherent information in UP and SP regarding the lenght of the primary sequence! Protein removed\n")
        file4.close()
        list_an.remove(an)
        file1=open(sys.argv[1], "w")
        for num in list_an:
            file1.write(num+"\n")
        file1.close()