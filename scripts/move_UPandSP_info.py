#!/usr/bin/env python3

# this program takes in input the file combined with all the AF informations and the file previously obtained for each
# proteins in the human proteome,  returning a file with a fixed header and a line for each residue in the  database format 

def add_to_list(category, content, residues, list_x, std, x="note"):
    if category==std:
        if std=="ACT_SITE" and x not in content:
            for i in residues:
                list_x[i]=list_x[i]+" Active Site"
        if content.split("=")[0]==x:
            for i in residues:
                list_x[i]=list_x[i]+" "+content.split("=")[1]
            while content[-1]!='"':
                new=next(file)
                row=new.split("\n")[0]
                content=row.split("                   ")[1]
                for i in residues:
                    list_x[i]=list_x[i]+" "+content

def add_to_single(category, residues, list_x, std):
    if category==std:
        for i in residues:
            list_x[i]=std

def not_found(list_x, i, abc):
    if list_x[i]=="[":
        list_x[i]=list_x[i]+" "+abc
    list_x[i]=list_x[i]+" ]"

import itertools
import sys
name_file_input=sys.argv[1]
ann=name_file_input.split("/")[-1]
an=ann.split("_")[0]
name_file_output=sys.argv[3]
file=open(sys.argv[2], "r")
ceck=False
found=False
list_variants=list(itertools.repeat("[", 50000))
list_domains=list(itertools.repeat("[", 50000))
list_chains=list(itertools.repeat("CHAIN", 50000))
list_mem=list(itertools.repeat("EXTRAMEM", 50000))
list_motives=list(itertools.repeat("[", 50000))
list_binding=list(itertools.repeat("[", 50000))
list_active=list(itertools.repeat("[", 50000))
list_mod_res=list(itertools.repeat("[", 50000))
list_carb=list(itertools.repeat("[", 50000))
list_lipid=list(itertools.repeat("[", 50000))
list_region=list(itertools.repeat("[", 50000))
list_cross=list(itertools.repeat("[", 50000))
list_ss=list(itertools.repeat("unk", 50000))
list_disulfide=list(itertools.repeat("no_bridge", 50000))
residues=None
for line in file:
    quary="AN   VALID ACCESSION: "+an
    if line.split(";")[0]==quary:
        ceck=True
        found=True
        print("found")
    if ceck and line=="//\n":
        ceck=False
        break
    if ceck and line[0:2]=="FT" and line[5]!=" ":
        l8=line.split("\n")[0]
        l7=l8.replace("        ", " ")
        l6=l7.replace("       ", " ")
        l5=l6.replace("      ", " ")
        l4=l5.replace("     ", " ")
        l3=l4.replace("    ", " ")
        l2=l3.replace("   ", " ")
        l1=l2.replace("  ", " ")
        x=(l1.split(" ")[1])
        if x in ['VARIANT', 'DOMAIN', 'SIGNAL', 'TRANSIT', 'PROPEP', 'TRANSMEM', 'INTRAMEM', 'MOTIF', 'BINDING', 'ACT_SITE', 'MOD_RES', 'CARBOHYD', 'LIPID', 'DISULFID', 'REGION', 'HELIX', 'STRAND', 'TURN', 'CROSSLNK']:
            category=x
            span=(l1.split(" ")[2])
            if an in span:
                residues=[0]
            elif "?" in span:
                residues=[0]
            else:
                if ".." in span:
                    pre2=span.split("..")[0]
                    pre1=pre2.replace("<", "")
                    pre=pre1.replace(">", "")
                    if not pre.isdigit():
                        print(an+": bug "+pre)
                    post2=span.split("..")[1]
                    post1=post2.replace("<", "")
                    post=post1.replace(">", "")
                    if not post.isdigit():
                        print(an+": bug "+pre)
                    residues=list(range(int(pre), int(post)+1))
                else:
                    residues=[int(span)]
        else:
            category="None"
        add_to_single(category, residues, list_chains, std="SIGNAL")
        add_to_single(category, residues, list_chains, std="TRANSIT")
        add_to_single(category, residues, list_mem, std="TRANSMEM")
        add_to_single(category, residues, list_mem, std="INTRAMEM")
        add_to_single(category, residues, list_ss, std="HELIX")
        add_to_single(category, residues, list_ss, std="STRAND")
        add_to_single(category, residues, list_ss, std="LOOP")
        if category=="DISULFID":
            first=residues[0]
            last=residues[-1]
            list_disulfide[first]="SS_BOND_"+str(last)
            list_disulfide[last]="SS_BOND_"+str(first)
    if ceck and line[0:2]=="FT" and line[5]==" " and category!="None" and ("/" in line):
        row=line.split("\n")[0]
        content=row.split("/", 1)[1]
        if category=="VARIANT":
            if content.split("=")[0]=="note":
                while content[-1]!='"':
                    new=next(file)
                    row=new.split("\n")[0]
                    new_content=row.split("                   ")[1]
                    content=content+new_content
                a=content.split("=")[1]
                if (a.split(" ")[0]=='"Missing') or ('"Missing"' in a):
                    for i in residues:
                        list_variants[i]=list_variants[i]+" del"
                else:
                    if len(a.split(" ")[0])==2:
                        mutation=a.split(" ")[2]
                        for i in residues:
                            list_variants[i]=list_variants[i]+" "+mutation
                    else:
                        res=residues[0]
                        l=len(a.split(" ")[0])-1
                        residues=list(range(int(res), int(res)+l))
                        mutation=a.split(" ")[2]
                        for i in residues:
                            if (i-res)<len(mutation):
                                list_variants[i]=list_variants[i]+" "+mutation[i-res]
                            else:
                                list_variants[i]=list_variants[i]+" del"
            if content.split("=")[0]=="id":
                for i in residues:
                    list_variants[i]=list_variants[i]+"_"+content.split("=")[1]
        add_to_list(category, content, residues, list_domains, std="DOMAIN")
        if category=="PROPEP":
            if content.split("=")[0]=="note":
                for i in residues:
                    list_chains[i]="PRO_"+content.split("=")[1]
        add_to_list(category, content, residues, list_motives, std="MOTIF")
        add_to_list(category, content, residues, list_binding, std="BINDING", x="ligand")
        add_to_list(category, content, residues, list_active, std="ACT_SITE")
        add_to_list(category, content, residues, list_mod_res, std="MOD_RES")
        add_to_list(category, content, residues, list_carb, std="CARBOHYD")
        add_to_list(category, content, residues, list_lipid, std="LIPID")
        add_to_list(category, content, residues, list_region, std="REGION")
        add_to_list(category, content, residues, list_cross, std="CROSSLNK")
file.close()
if not found:
    print("not_found")
    list_chains=list(itertools.repeat("unk", 50000))
    list_mem=list(itertools.repeat("unk", 50000))
file1=open(name_file_input, "r")
file2=open(name_file_output, "w")
for _ in [1, 2, 3, 4, 5, 6]:
    line=next(file1)
    file2.write(line)
file2.write("\n\
# primary key (an_position)\n\
    #1: Uniprot reference proteome residue\n\
        #2: AlphaFold residue\n\
            #3: UniProt annotated natural variants\n\
                #4: signal-peptide/transit-peptide/pro-peptide/chain\n\
                    #5: loclization with respect to membranes\n\
                        #6: UniProt annotated motives\n\
                            #7: UniProt annotated domains\n\
                                #8: UniProt annotated ligands (binding site)\n\
                                    #9: UniProt annotated properties (active site)\n\
                                        #10: list of annotated Phosphosite PTMs\n\
                                            #11: UniProt annotated glycosylations\n\
                                                #12: UniProt annotated lipidations\n\
                                                    #13: UniProt annotated modifyed residues\n\
                                                        #14: UniProt annotated disulfide-dond bridges\n\
                                                            #15: UniProt annotated secondary structure\n\
                                                                #16: AlphaFold predicted secondary structure\n\
                                                                    #17: AlphaFold confidence value\n\
                                                                        #18: AlphaFold maximum predicted number of interacting residues in a single structure (r = 8A)\n\
                                                                            #19: AlphaFold list of residue with a predicted interaction in at least one structure (r = 8A)\n\
                                                                                #20: UniProt annotated crosslinks\n\n\n")
for line in file1:
    if line[0]=="A":
        pos1=line.split(" ")[0]
        pos=int(pos1.split("A")[1])
        not_found(list_variants, pos, abc="no_variant")
        not_found(list_mod_res, pos, abc="no_mod_res")
        not_found(list_domains, pos, abc="no_domain")
        not_found(list_motives, pos, abc="no_motive")
        not_found(list_binding, pos, abc="no_ligand")
        not_found(list_active, pos, abc="no_active_site")
        not_found(list_carb, pos, abc="no_carbohydrate")
        not_found(list_lipid, pos, abc="no_lipid")
        not_found(list_region, pos, abc="no_ann_region")
        not_found(list_cross, pos, abc="no_crosslink")
        row=line.split("\n")[0]
        res_UP=row.split("  ")[1]
        res_AF=row.split("  ")[2]
        precision_AF=row.split("  ")[3]
        if precision_AF=="unk.00":
            precision_AF="unk"
        ss_AF=row.split("  ")[4]
        number_contacts_AF=row.split("  ")[5]
        l4=row.split("[")[1]
        l3=l4.split("]")[0]
        l2=l3.replace("    ", " ")
        l1=l2.replace("   ", " ")
        list_contacts_AF=l1.replace("  ", " ")
        if list_contacts_AF==" ":
            list_contacts_AF==" no_contacts "
        l4=row.split("[")[2]
        l3=l4.split("]")[0]
        l2=l3.replace("    ", " ")
        l1=l2.replace("   ", " ")
        list_PTMs=l1.replace("  ", " ")
        if list_PTMs==" ":
            list_PTMs==" no_PTMs "
        file2.write(an+"_"+str(pos)+" | 1: "+res_UP+" | 2: "+res_AF+" | 3: "+list_variants[pos]+" | 4: "+list_chains[pos]+\
                    " | 5: "+list_mem[pos]+" | 6: "+list_motives[pos]+" | 7: "+list_domains[pos]+" | 8: "+list_binding[pos]+\
                    " | 9: "+list_active[pos]+" | 10: ["+list_PTMs+"] | 11: "+list_carb[pos]+" | 12: "+list_lipid[pos]+\
                    " | 13: "+list_mod_res[pos]+" | 14: "+list_disulfide[pos]+" | 15: "+list_ss[pos]+" | 16: "+ss_AF+\
                    " | 17: "+precision_AF+" | 18: "+number_contacts_AF+" | 19: ["+list_contacts_AF+"] | 20: "+list_cross[pos]+"\n")
file1.close()
file2.close()