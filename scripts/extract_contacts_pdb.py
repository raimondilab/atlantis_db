#!/usr/bin/env python3

def custom_sort(code):
    # Split the code into alphanumeric and numeric parts
    alpha_part1, alpha_part2, num_part = code.split('_')
    alpha_part=alpha_part1+alpha_part2
    num_part = int(num_part)
    #print(alpha_part)
    #print(num_part)
    return (alpha_part, num_part)

import sys
import os
import itertools
pdb_list=[]
residue_list={}
ac_list=[]
pdb_code=sys.argv[1]
pre_existing_contacts=[""]
workdir=sys.argv[5]
file3=open(sys.argv[3], "r")
for line in file3:
    pdb_list.append(line.split("\n")[0])
file3.close()
file4=open(sys.argv[4], "r")
next(file4)
for line in file4:
    if line=="\n":
        break
    row=line.split("|")[0]
    if ((row.split("\t")[0])+"_"+(row.split("\t")[1])) in pdb_list:
        r=line.split("\n")[0]
        row=r.split("|")[1]
        key=row.split("\t")[0]
        number=r.split("\t")[3]
        residue_list[key[3:]]=(row.split("\t")[1])+"_"+(number[1:])
        if row.split("\t")[1] not in ac_list:
            ac_list.append(row.split("\t")[1])
file4.close()
for ac in ac_list:
    file2=open(sys.argv[2], "r")
    protein=list(itertools.repeat("", 50000))
    last_residue=0
    for line in file2:
        if len(line.split(" "))==1:
            break
        res1=line.split(" ")[0]
        res2=line.split(" ")[1]
        r1=res1.split("/")[1]
        r2=res2.split("/")[1]
        if (r1 in residue_list) and (r2 in residue_list):
            if ac in residue_list[r1]:
                a=residue_list[r1]
                protein[int(a.split("_")[1])]=protein[int(a.split("_")[1])]+pdb_code+"_"+residue_list[r2]+" "
                if int(a.split("_")[1])>last_residue:
                    last_residue=int(a.split("_")[1])
            if ac in residue_list[r2]:
                a=residue_list[r2]
                protein[int(a.split("_")[1])]=protein[int(a.split("_")[1])]+pdb_code+"_"+residue_list[r1]+" "
                if int(a.split("_")[1])>last_residue:
                    last_residue=int(a.split("_")[1])
    file2.close()
    name_file=workdir+ac+"_pdb_contacts.txt"
    if os.path.exists(name_file):
        file5=open(name_file, "r")
        for line in file5:
            if " " in line:
                position=int(line.split(" ")[0])
                row=line.split(" ", 1)[1]
            else:
                position=int(line.split("\n")[0])
                row="\n"
            protein[position]=protein[position]+row.split("\n")[0]
            if position>last_residue:
                last_residue=position
        file5.close()
    file5=open(name_file, "w")
    for l in range(1, last_residue+1):
        text=protein[int(l)]
        out=text.split(" ")
        if "" in out:
            out.remove("")
        single_copy=list(set(out))
        ordered_single_copy=sorted(single_copy, key=custom_sort)
        #print(ordered_single_copy)
        file5.write(str(l))
        if len(ordered_single_copy)>0:
            for element in ordered_single_copy:
                file5.write(" "+element)
        file5.write("\n")
    file5.close()