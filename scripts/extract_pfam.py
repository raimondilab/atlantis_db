#!/usr/bin/env python3

import sys
file1=open(sys.argv[1], "r")
folder=sys.argv[2]
temp=[]
new_domain=True
for line in file1:
    if new_domain:
        temp.append(line)
    if line[0:4]=="ACC " and new_domain:
        if "." in line:
            row=line.split(".")[0]
        else:
            row=line.split("\n")[0]
        pfam_number="PF"+row.split("PF")[1]
        name_file=folder+"/"+pfam_number+"_HMM.txt"
        file2=open(name_file, "w")
        print(name_file)
        for element in temp:
            file2.write(element)
        temp=[]
        new_domain=False
        continue
    if line=="//\n":
        new_domain=True
        file2.write("//")
        file2.close()
        continue
    if not new_domain:
        file2.write(line)
file1.close()