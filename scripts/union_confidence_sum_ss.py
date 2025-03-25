#/usr/bin/env python3

# this program takes in input one file at the time and cecks if there is one file "complete" for that protein:
# if it exists, the information are added, oterwise the file is created
# the "complete" has no header and contains a list of all the residue in the protein the the form:
# "Aposition residue sum_of_confidence_values number_of_value_summed consensus_seconday_structure"

import sys
import itertools
name_file_input=sys.argv[1]
file1=open(name_file_input, "r")
number=int(name_file_input.split("-")[1])
if number==1:
    name_file_output=name_file_input.split("-001")[0]+"_complete_sumconf_ss.txt"
    file2=open(name_file_output, "a")
    for line in file1:
        if line!="\n":
            file2.write(line.split(" ")[0]+" "+line.split(" ")[1]+" "+line.split(" ")[2]+" "+"1 "+line.split(" ")[3])
    file2.close()
else:
    name_file_output=name_file_input.split("-")[0]+"_complete_sumconf_ss.txt"
    file2=open(name_file_output, "r")
    ss=list(itertools.repeat("unk", 100000))
    f2=list(itertools.repeat(0, 100000))
    f5=list(itertools.repeat(0, 100000))
    f6=list(itertools.repeat("X", 100000))
    i=0
    for line in file2:
        if line!="\n":
            res=float(line.split(" ")[2])
            times_seen=int(line.split(" ")[3])
            type=line.split(" ")[1]
            structure=line.split(" ")[4]
            ss[i]=structure.split("\n")[0]
            f2[i]=res
            f5[i]=times_seen
            f6[i]=type
            i=i+1
    file2.close()
    file2=open(name_file_output, "w")
    for i in range (0, (200*(number-1))):
        file2.write("A"+str(i+1)+" "+f6[i]+" "+str(f2[i])+" "+str(f5[i])+" "+ss[i]+"\n")
    i=0
    for line in file1:
        sum=float((line.split(" ")[2]))+(f2[i+(200*(number-1))])
        file2.write("A"+str(i+(200*(number-1))+1)+" "+line.split(" ")[1]+" "+str(round(sum, 2))+" "+str(f5[i+(200*(number-1))]+1))
        pre_ss=line.split(" ")[3]
        if (ss[i+(200*(number-1))]=="unk"):
            file2.write(" "+pre_ss.split("\n")[0]+"\n")
        elif ((pre_ss.split("\n")[0])=="unk"):
            file2.write(" "+ss[i+(200*(number-1))]+"\n")
        elif (i>=200) and ((pre_ss.split("\n")[0])!=ss[i+(200*(number-1))]):
            file2.write(" ?\n")
        else:
            file2.write(" "+ss[i+(200*(number-1))]+"\n")
        i=i+1
    file2.close()
file1.close()