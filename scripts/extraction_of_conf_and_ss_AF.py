#/usr/bin/env python3

# tis program parses a AF structure file and returns a file hwith no header
# that contains a list of all the residue in the protein in the form:
# "Aposition residue confidence_value seconday_structure"

def change_name(aa):
    if aa=="ASP":
        a="D"
    elif aa=="GLU":
        a="E"
    elif aa=="ALA":
        a="A"
    elif aa=="ARG":
        a="R"
    elif aa=="ASN":
        a="N"
    elif aa=="CYS":
        a="C"
    elif aa=="PHE":
        a="F"
    elif aa=="GLY":
        a="G"
    elif aa=="GLN":
        a="Q"
    elif aa=="ILE":
        a="I"
    elif aa=="HIS":
        a="H"
    elif aa=="LEU":
        a="L"
    elif aa=="LYS":
        a="K"
    elif aa=="MET":
        a="M"
    elif aa=="PRO":
        a="P"
    elif aa=="SER":
        a="S"
    elif aa=="TYR":
        a="Y"
    elif aa=="THR":
        a="T"
    elif aa=="TRP":
        a="W"
    elif aa=="VAL":
        a="V"
    else:
        a="X"
    return a

import gzip
import sys
import itertools
list_an=[]
ss=list(itertools.repeat("unk", 50000))
confidence=[]
last_res=0
file=open(sys.argv[3], "r")
for line in file:
    an=line.split("\n")[0]
    list_an.append(an)
file.close()
name_file_input=sys.argv[1]
workdir=sys.argv[2]
file1=gzip.open(name_file_input, "rt")
a=name_file_input.split("F-", 1)[1]
an=a.split("-F")[0]
n=a.split("-F")[1]
number=int(n.split("-model")[0])
if number<=9:
    name_file_output=(workdir+an+"-00"+str(number)+"-AF_confidence_secondary_structure_list.txt")
elif number<=99:
    name_file_output=(workdir+an+"-0"+str(number)+"-AF_confidence_secondary_structure_list.txt")
else:
    name_file_output=(workdir+an+"-"+str(number)+"-AF_confidence_secondary_structure_list.txt")
if an in list_an:
    control=False
    for line in file1:
        if control:
            if line=="#\n":
                break
        if control:
            l1=line.replace("     ", " ")
            l2=l1.replace("    ", " ")
            l3=l2.replace("   ", " ")
            l4=l3.replace("  ", " ")
            confidence.append("A"+l4.split(" ")[2]+" "+change_name(l4.split(" ")[1])+" "+l4.split(" ")[4])
        if line=="_ma_qa_metric_local.ordinal_id\n":
            print("_ma_qa_metric_local.ordinal_id")
            control=True
    file1.close()
    file1=gzip.open(name_file_input, "rt")
    ceck=False
    for line in file1:
        if ceck:
            if line=="#\n":
                break
        if ceck:
            l11=line.replace("            ", " ")
            l10=l11.replace("           ", " ")
            l9=l10.replace("          ", " ")
            l8=l9.replace("         ", " ")
            l7=l8.replace("        ", " ")
            l6=l7.replace("       ", " ")
            l5=l6.replace("      ", " ")
            l4=l5.replace("     ", " ")
            l3=l4.replace("    ", " ")
            l2=l3.replace("   ", " ")
            l1=l2.replace("  ", " ")
            x=(l1.split(" ")[6]+"_")
            for i in range(last_res+1, int(l1.split(" ")[5])):
                ss[i]="unk"
            for i in range(int(l1.split(" ")[5]), int(l1.split(" ")[12])+1):
                ss[i]=x.split("_")[0]
            last_res=int(l1.split(" ")[12])
        if line=="_struct_conf.pdbx_end_PDB_ins_code\n":
            print("_struct_conf.pdbx_end_PDB_ins_code")
            ceck=True
    file1.close()
    file2=open(name_file_output, "w")
    i=1
    for element in confidence:
        file2.write(element+" "+ss[i]+"\n")
        i=i+1
    file2.close()