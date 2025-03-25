#!/usr/bin/env python3

import sys
list=[]
list_an=[]
file=open(sys.argv[1], "r")
for line in file:
    an=line.split("\n")[0]
    list_an.append(an)
file.close()
for l in range(2, 9):
    name_file_input=sys.argv[l]
    file=open(name_file_input, "r")
    for line in file:
        if "human" in line:
            an=line.split("\t")[2]
            if an in list_an:
                residuo=line.split("\t")[4]
                aminoacido=residuo[0]
                n1=residuo.split("-")[0]
                n2=int(n1[1:])
                if n2<=9:
                    s=line.split("\t")[2]+" "+"0000"+str(n2)+" "+n1[0]+" "+residuo.split("-")[1]
                elif n2<=99:
                    s=line.split("\t")[2]+" "+"000"+str(n2)+" "+n1[0]+" "+residuo.split("-")[1]
                elif n2<=999:
                    s=line.split("\t")[2]+" "+"00"+str(n2)+" "+n1[0]+" "+residuo.split("-")[1]    
                elif n2<=9999:
                    s=line.split("\t")[2]+" "+"0"+str(n2)+" "+n1[0]+" "+residuo.split("-")[1]
                elif n2<=99999:
                    s=line.split("\t")[2]+" "+str(n2)+" "+n1[0]+" "+residuo.split("-")[1]
                list.append(s)
    file.close()
list.sort()
name_file_output="PTM_output.txt"
file=open(name_file_output, "w")
for element in list:
    file.write(element+"\n")
file.close()