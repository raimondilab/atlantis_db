#!/usr/bin/env python3

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

import gzip
import sys
list=[]
ans=[]
file=open(sys.argv[1], "r")
for line in file:
    list.append(line.split("\n")[0])
file.close()
file2=open(sys.argv[2], "w")
file1=gzip.open(sys.argv[3], "rt")
ceck=False
ceck1=False
string_an=""
reading=False
for line in file1:
    if line.split("   ")[0]=="ID":
        specie=line.split("_")[1]
        if specie.split(" ")[0]=="HUMAN":
            ceck=True
            id=line
    if ceck and line.split("   ")[0]=="AC":
        an=line.split("   ")[1]
        string_an=string_an+(an.split(";\n")[0])+"; "
        reading=True
    if ceck and reading and line.split("   ")[0]=="":
        an=line.split("   ")[1]
        string_an=string_an+(an.split(";\n")[0])+"; "
        reading=True
    if ceck and reading and line.split("   ")[0]!="AC" and line.split("   ")[0]!="":
        reading=False
        list_an=string_an.split("; ")
        list_an.remove("")
        ans=intersection(list, list_an)
        if ans!=[]:
            ceck1=True
            file2.write("\n//\n\n"+id)
            file2.write("AN   VALID ACCESSION: ")
            for element in ans:
                file2.write(element+"; ")
                list.remove(element)
            file2.write("\n")
            file2.write("AC   ")
            for element in list_an:
                file2.write(element+"; ")
            file2.write("\n")
    if line.split("\n")[0]=="//":
        ceck=False
        ceck1=False
        reading=False
        string_an=""
    if ceck and ceck1 and not(reading):
        file2.write(line)
file1.close()
file1=gzip.open(sys.argv[4], "rt")
ceck=False
ceck1=False
string_an=""
reading=False
for line in file1:
    if line.split("   ")[0]=="ID":
        specie=line.split("_")[1]
        if specie.split(" ")[0]=="HUMAN":
            ceck=True
            id=line
    if ceck and line.split("   ")[0]=="AC":
        an=line.split("   ")[1]
        string_an=string_an+(an.split(";\n")[0])+"; "
        reading=True
    if ceck and reading and line.split("   ")[0]=="":
        an=line.split("   ")[1]
        string_an=string_an+(an.split(";\n")[0])+"; "
        reading=True
    if ceck and reading and line.split("   ")[0]!="AC" and line.split("   ")[0]!="":
        reading=False
        list_an=string_an.split("; ")
        list_an.remove("")
        ans=intersection(list, list_an)
        if ans!=[]:
            ceck1=True
            file2.write("\n//\n\n"+id)
            file2.write("AN   VALID ACCESSION: ")
            for element in ans:
                file2.write(element+"; ")
                list.remove(element)
            file2.write("\n")
            file2.write("AC   ")
            for element in list_an:
                file2.write(element+"; ")
            file2.write("\n")
    if line.split("\n")[0]=="//":
        ceck=False
        ceck1=False
        reading=False
        string_an=""
    if ceck and ceck1 and not(reading):
        file2.write(line)
file1.close()
file2.close()
file4=open(sys.argv[5], "a")
file4.write("List of protein with no information from UniProt or SwissProt: ")
for element in list:
    file4.write(element+" ")
file4.write("\n")
file4.close()