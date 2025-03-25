#!/usr/bin/env python3

# this program takes the information contained in the pdbs and for every protin in the human protein assigns
# to each residue, all the residues (in that protein or in any other) at the condistion that there is at least one
# pdb fil where those two residues are in contact: it's specifyed the residue position and chain (UP accession), and
# the PDB where this interaction is observed

def replacing_function(row):
    row=row.replace("#20", "    #21")
    row=row.replace("#19", "    #20")
    row=row.replace("#18", "    #19")
    row=row.replace("#17", "    #18")
    row=row.replace("#16", "    #17")
    row=row.replace("#15", "    #16")
    row=row.replace("#14", "    #15")
    row=row.replace("#13", "    #14")
    row=row.replace("#12", "    #13")
    row=row.replace("#11", "    #12")
    row=row.replace("#10", "    #11")
    row=row.replace("#9", "    #10")
    row=row.replace("#8", "    #9")
    row=row.replace("#change", "#8")
    row=row.replace(" | 20: ", " | 21: ")
    row=row.replace(" | 19: ", " | 20: ")
    row=row.replace(" | 18: ", " | 19: ")
    row=row.replace(" | 17: ", " | 18: ")
    row=row.replace(" | 16: ", " | 17: ")
    row=row.replace(" | 15: ", " | 16: ")
    row=row.replace(" | 14: ", " | 15: ")
    row=row.replace(" | 13: ", " | 14: ")
    row=row.replace(" | 12: ", " | 13: ")
    row=row.replace(" | 11: ", " | 12: ")
    row=row.replace(" | 10: ", " | 11: ")
    row=row.replace(" | 9: ", " | 10: ")
    row=row.replace(" | 8: ", " | 9: ")
    row=row.replace(" | change: ", " | 8: ")
    return row

import sys
import itertools
import os
file1=open(sys.argv[1], "r")
protein=sys.argv[3]
domain=sys.argv[4]
folder=sys.argv[5]
workdir=sys.argv[6]
ranges=[]
for line in file1:
    if line!="\n":
        ranges.append(line.split("\n")[0])
file1.close()
residues=list(itertools.repeat(0, 50000))
file2=open(sys.argv[2], "r")
for line in file2:
    if "Query" in line:
        row=line.replace("        ", " ")
        row=row.replace("       ", " ")
        row=row.replace("      ", " ")
        row=row.replace("     ", " ")
        row=row.replace("    ", " ")
        row=row.replace("   ", " ")
        row=row.replace("  ", " ")
        header2=row.split(" ")[1]
    elif "Domain annotation for each sequence (and alignments):" in line:
        a=next(file2)
        if ">> " in a:
            header1=a.split(" ")[1]
        else:
            header1="sp|"+protein
        continue
    elif "Alignments for each domain:" not in line:
        continue
    else:
        break
new_domain1=True
new_domain2=True
beginning=0
ending=0
start=0
sequence=""
ref_sequence=""
copy_ref=[]
for line in file2:
    if (new_domain1) and (header1 in (line)):
        row=line.split(header1, 1)[1]
        row=row.replace("    ", " ")
        row=row.replace("   ", " ")
        row=row.replace("  ", " ")
        row=row.replace("\n", "")
        beginning=int(row.split(" ")[1])
        sequence=row.split(" ")[2]
        if row.split(" ")[3]=="-":
            ending=beginning
        else:
            ending=int(row.split(" ")[3])
        new_domain1=False
    elif (new_domain2) and (header2 in (line)):
        row=line.split(header2, 1)[1]
        row=row.replace("      ", " ")
        row=row.replace("     ", " ")
        row=row.replace("    ", " ")
        row=row.replace("   ", " ")
        row=row.replace("  ", " ")
        row=row.replace("\n", "")
        try:
            start=int(row.split(" ")[1])
        except ValueError:
            continue
        except IndexError:
            continue
        ref_sequence=row.split(" ")[2]
        new_domain2=False
    elif (not new_domain1) and (header1 in (line)):
        row=line.split(header1, 1)[1]
        row=row.replace("    ", " ")
        row=row.replace("   ", " ")
        row=row.replace("  ", " ")
        row=row.replace("\n", "")
        sequence=sequence+row.split(" ")[2]
        if row.split(" ")[1]!="-":
            if (int(row.split(" ")[1]))>(ending+1):
                for i in range(ending+1, (int(row.split(" ")[1]))):
                    sequence=sequence+"-"
        if row.split(" ")[3]!="-":
            ending=int(row.split(" ")[3])
    elif (not new_domain2) and (header2 in (line)):
        row=line.split(header2, 1)[1]
        row=row.replace("      ", " ")
        row=row.replace("     ", " ")
        row=row.replace("    ", " ")
        row=row.replace("   ", " ")
        row=row.replace("  ", " ")
        row=row.replace("\n", "")
        try:
            a=int(row.split(" ")[1])
        except ValueError:
            continue
        except IndexError:
            continue
        ref_sequence=ref_sequence+row.split(" ")[2]
    elif "== domain" in line:
        new_domain1=True
        new_domain2=True
        count=start
        for i in range(0, len(ref_sequence)):
            if ref_sequence[i]!=".":
                copy_ref.append(count)
                count=count+1
            else:
                copy_ref.append(0)
        for section in ranges:
            rg=section.split("\n")[0]
            if beginning>=int(rg.split("   ")[0]) and ending<=int(rg.split("   ")[1]):
                j=0
                for i in range(0, len(copy_ref)):
                    if sequence[i]!="-":
                        residues[beginning+j]=copy_ref[i]
                        j=j+1
                    i=i+1
        copy_ref=[]
    else:
        pass
count=start
for i in range(0, len(ref_sequence)):
    if ref_sequence[i]!=".":
        copy_ref.append(count)
        count=count+1
    else:
        copy_ref.append(0)
for section in ranges:
    rg=section.split("\n")[0]
    if beginning>=int(rg.split("   ")[0]) and ending<=int(rg.split("   ")[1]):
        j=0
        for i in range(0, len(copy_ref)):
            if sequence[i]!="-":
                residues[beginning+j]=copy_ref[i]
                j=j+1
            i=i+1
if os.path.isfile(workdir+"/"+protein+"_residues_UPinfos_PFAM_PTMs_AF.txt"):
    file3=open(workdir+"/"+protein+"_residues_UPinfos_PFAM_PTMs_AF.txt", "r")
else:
    file3=open(folder+"/"+protein+"_residues_UPinfos_PTMs_AF.txt", "r")
content=[]
renew=True
for line in file3:
    if "#7:" in line:
        content.append("                            #7: UniProt annotated domains\n")
    elif "#8:" in line:
        if "ligands (binding site)" in line:
            content.append("                                #change: PFAM domain and alligned position in the HMM\n"+line)
        else:
            content.append(line)
            renew=False
    elif ((protein+"_") in line) and ("HUMAN;" not in line):
        num=line.split("_", 1)[1]
        n=int(num.split(" ")[0])
        if renew:
            if residues[n]!=0:
                content.append(line.split("] | 8:")[0]+"] | change: [ "+domain+"_"+str(residues[n])+" ] | 8:"+line.split("] | 8:")[1])
            else:
                content.append(line.split("] | 8:")[0]+"] | change: [ no_PFAM_res ] | 8:"+line.split("] | 8:")[1])
        else:
            if residues[n]!=0:
                if "[ no_PFAM_res ]" in line:
                    content.append(line.split("no_PFAM_res")[0]+domain+"_"+str(residues[n])+" ] | 9:"+line.split("] | 9:")[1])
                else:
                    content.append(line.split("] | 9:")[0]+domain+"_"+str(residues[n])+" ] | 9:"+line.split("] | 9:")[1])
            else:
                content.append(line)
    else:
        content.append(line)
file3.close()
file4=open(workdir+"/"+protein+"_residues_UPinfos_PFAM_PTMs_AF.txt", "w")
for element in content:
    if renew:
        output_string=replacing_function(element)
        file4.write(output_string)
    else:
        file4.write(element)
file4.close()