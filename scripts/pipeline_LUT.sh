#!/bin/bash    
#PBS -l select=1:ncpus=20:mem=25gb  
#PBS -l walltime=168:00:00
#PBS -q q07anacreon
#PBS -N pipeline_LUT


# THIS FIRST PART OF THE SCRIPT NEEDS TO BE SATTISFIEDY PRIOR TO START THE PIPELINE


mkdir /home/pferronato/scripts/pipeline_scripts/workdir/
workdir="/home/pferronato/scripts/pipeline_scripts/workdir" # insert temporary directory
script_directory="/home/pferronato/scripts/pipeline_scripts" # insert the directory containing the scripts

# there is the need to get the Human Proteome database form UniProt in the $workdir
# please, download the database in the directory $workdir from the link https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/UP000005640/UP000005640_9606.fasta.gz

# there is the need to get the PTMs' databases form PhosphoSite in the $workdir
# please, download the seven databases in the directory $workdir from the link https://www.phosphosite.org/staticDownloads

source_AF="/projects/bioinformatics/DB/AlphaFold_EBI/UP000005640_9606_HUMAN_v4" # insert position AF structures files
uniprot_database="/projects/bioinformatics/DB/uniprot/complete/uniprot_trembl.dat.gz" # insert the path tho the database "uniprot_sprot.dat.gz"
swissprot_database="/projects/bioinformatics/DB/uniprot/complete/uniprot_sprot.dat.gz" # insert the path tho the database "uniprot_trembl.dat.gz"
source_HHM="/projects/bioinformatics/DB/PFAM/Pfam-A.hmm" # insert the path tho the HMM calculator
source_human_domains="/projects/bioinformatics/DB/PFAM/9606.tsv" # insert the path to the file containing the list of PFAM domains in the human proteome
source_human_pdb="/projects/bioinformatics/DB/SIFTS/pdb_chain_taxonomy.tsv.gz" # insert the path to the file containing the list of human chains in pdbs
source_PDB="/projects/bioinformatics/DB/pdb-mmCIF_CBcontacts" # insert position PDB structures files


# NOW THIS PIPELINE CAN BE LAUNCHED


mkdir $workdir/AlphaFold_contacts/
workdir_AF_contacts="${workdir}/AlphaFold_contacts"
mkdir $workdir/AlphaFold_confidence_and_ss/
workdir_AF_confidence_and_ss="${workdir}/AlphaFold_confidence_and_ss"
mkdir $workdir/AlphaFold/
workdir_AF="${workdir}/AlphaFold"
mkdir $workdir/PFAM/
workdir_PFAM="${workdir}/PFAM"
mkdir $workdir/PDB/
workdir_PDB="${workdir}/PDB"
touch $workdir/follow_LUT_pipleline_process.txt
echo "start" >> $workdir/follow_LUT_pipleline_process.txt


cd $workdir


# firts of all we have to extract a list of all the accession numbers from the file containig
# the FASTA sequence for the whole human genome

gunzip $workdir/*_9606.fasta.gz
human_proteome_FASTA=""
n=0
for dataset in `ls $workdir | grep _9606.fasta`
do
  human_proteome_FASTA="${dataset}"
  n=$((n+1))
done
if [ $n -eq 1 ]
then
  touch $workdir/human_an_list.txt
  python3 $script_directory/extraction_of_human_proteome.py $workdir/$human_proteome_FASTA $workdir/human_an_list.txt
else
  echo "wrong number of UniProt databases"
  exit[1]
fi
wait

echo "Creatred files FASTAs and an_list" >> $workdir/follow_LUT_pipleline_process.txt


# second of all, from the databases, the PTMs are now going to be extracted

gunzip $workdir/*_site_dataset.gz
argument="${workdir}/human_an_list.txt"
n=0
for dataset in `ls $workdir | grep _site_dataset`
do
  argument="${argument} ${workdir}/${dataset}"
  n=$((n+1))
done
if [ $n -eq 7 ]
then
  touch $workdir/PTM_output.txt
  python3 $script_directory/script_extraction_PTM.py $argument
else
  echo "wrong number of PhosphoSite databases"
  exit[1]
fi
wait
gzip $workdir/*_site_dataset
wait

echo "Created file PTMs" >> $workdir/follow_LUT_pipleline_process.txt


# this part will extract the contacts form the AF structures retrning a file for every structure

n=0
for structure in `ls -1 $source_AF | grep cif.gz`
do
  structureout=`echo $structure | cut -f 7 -d "/"`
  if [ ! -f "${structureout%%.cif.gz}_3dc.txt" ]
  then
    echo ${structureout%%.cif.gz}
    gunzip $source_AF/$structure
    if ((n < 40))
    then
      /home/pmiglionico/scripts/cifparse-obj-v7.105-prod-src/parser-test-app/bin/3DContact_hetatm $source_AF/${structure%%.gz} 8 > $workdir_AF_contacts/${structureout%%.cif.gz}_3dc.txt &
      n=$((n+1))
    else
      /home/pmiglionico/scripts/cifparse-obj-v7.105-prod-src/parser-test-app/bin/3DContact_hetatm $source_AF/${structure%%.gz} 8 > $workdir_AF_contacts/${structureout%%.cif.gz}_3dc.txt
      n=0
    fi
  fi
done
wait
cd $source_AF
gzip *
wait
cd $workdir

echo "Created files _3dc.txt in ${workdir_AF_contacts}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF_contacts | grep _3dc.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# this program simply renames the file to have them ordered alfabetically and by number in the folder

for element in `ls $workdir_AF_contacts | grep _3dc.txt`
do
  name=${element:3}
  number=$(awk -F'-F|-model' '{print $2}' <<< "$name")
  pre=$(awk -F'-F' '{print $1}' <<< "$name")
  if [ $((number)) -le 9 ]
  then
    new_name="AF_${pre}-F00${number}-model_v4_3dc_count_ord.txt"
  else
    if [ $((number)) -le 99 ]
    then
      new_name="AF_${pre}-F0${number}-model_v4_3dc_count_ord.txt"
    else
      new_name="AF_${pre}-F${number}-model_v4_3dc_count_ord.txt"
    fi
  fi
  cp $workdir_AF_contacts/$element $workdir_AF_contacts/$new_name
  rm $workdir_AF_contacts/$element
done
wait

echo "Created files model_v4_3dc_count_ord.txt in ${workdir_AF_contacts}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF_contacts | grep model_v4_3dc_count_ord.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# here for each file obtained by the analysis of the structure a new file is produced: the new file contain a list
# of all the residues with the number of contacts and the list of them

for element in `ls $workdir_AF_contacts | grep model_v4_3dc_count_ord.txt`
do
  if ((n < 40))
  then
    python3 $script_directory/count_and_list_AF_contacts.py $workdir_AF_contacts/$element &
    n=$((n+1))
  else
    python3 $script_directory/count_and_list_AF_contacts.py $workdir_AF_contacts/$element
    n=0
  fi
done
wait
rm $workdir_AF_contacts/*model_v4_3dc_count_ord.txt
wait

echo "Created files _3dc_list.txt in ${workdir_AF_contacts}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF_contacts | grep _3dc_list.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# since some proteins are divided in more then one structure this program groups them in one file

for element in `ls $workdir_AF_contacts | grep _3dc_list.txt`
do
  python3 $script_directory/union_files_AF_contacts.py $workdir_AF_contacts/$element $workdir/human_an_list.txt
done
wait
rm $workdir_AF_contacts/*_3dc_list.txt
wait

echo "Created files _complete_AF_contacts.txt in ${workdir_AF_contacts}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF_contacts | grep _complete_AF_contacts.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# this part will extract  confidence values and secondary structures form the AF

n=0
for structure in `ls -1 $source_AF | grep cif.gz`
do
  if ((n < 40))
  then
    python3 $script_directory/extraction_of_conf_and_ss_AF.py $source_AF/$structure $workdir_AF_confidence_and_ss/ $workdir/human_an_list.txt &
    n=$((n+1))
  else
    python3 $script_directory/extraction_of_conf_and_ss_AF.py $source_AF/$structure $workdir_AF_confidence_and_ss/ $workdir/human_an_list.txt
    n=0
  fi
done
wait

echo "Created files AF_confidence_secondary_structure_list.txt in ${workdir_AF_confidence_and_ss}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF_confidence_and_ss | grep AF_confidence_secondary_structure_list.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# since some proteins are divided in more then one structure this program groups them in one file

for element in `ls $workdir_AF_confidence_and_ss | grep AF_confidence_secondary_structure_list.txt`
do
  python3 $script_directory/union_confidence_sum_ss.py $workdir_AF_confidence_and_ss/$element
  rm $workdir_AF_confidence_and_ss/$element
done
wait

echo "Created files _complete_sumconf_ss.txt in ${workdir_AF_confidence_and_ss}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF_confidence_and_ss | grep _complete_sumconf_ss.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# this program unites the output of the two processes that have taken place

for element in `ls $workdir_AF_confidence_and_ss | grep _complete_sumconf_ss.txt`
do
  number=$(awk -F'_complete' '{print $1}' <<< "$element")
  file_contacts="AF_${number}_complete_AF_contacts.txt"
  new_name="${number}_complete_AF.txt"
  touch $workdir_AF/$new_name
  python3 $script_directory/avarage_confidence_sum_ss.py $workdir_AF_confidence_and_ss/$element $workdir_AF_contacts/$file_contacts $workdir_AF/$new_name
  rm $workdir_AF_confidence_and_ss/$element
  rm $workdir_AF_contacts/$file_contacts
done
wait
rmdir $workdir/AlphaFold_contacts/
rmdir $workdir/AlphaFold_confidence_and_ss/
wait

echo "Created files _complete_AF.txt in ${workdir_AF}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF | grep _complete_AF.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# the following part unites all the infor contained in teh previous file with the standard annotated residue in UniProt
# and all the PTMs contained in $workdir/PTM_output.txt

for element in `ls $workdir_AF | grep _complete_AF.txt`
do
  number=$(awk -F'_complete' '{print $1}' <<< "$element")
  new_name="${number}_complete_residues_AF_PTMs.txt"
  touch $workdir_AF/$new_name
  python3 $script_directory/fusion_AF_PTMs.py $workdir_AF/$element $workdir/$human_proteome_FASTA $workdir/PTM_output.txt $workdir_AF/$new_name $workdir/follow_LUT_pipleline_process.txt
  rm $workdir_AF/$element
done
wait

echo "Created files _complete_residues_AF_PTMs.txt in ${workdir_AF}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF | grep _complete_residues_AF_PTMs.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt

python3 $script_directory/fusion_noAF_PTMs.py $workdir/human_an_list.txt $workdir_AF/ $workdir/$human_proteome_FASTA $workdir/PTM_output.txt
wait

echo "Created files _complete_residues_AF_PTMs.txt in ${workdir_AF}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF | grep _complete_residues_AF_PTMs.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# the following part extract the information from UniProt and Swiss prot about all proteins in the human proteome

touch $workdir/UPandSP_info.txt
python3 $script_directory/extraxtion_of_info_from_SP_and_UP.py $workdir/human_an_list.txt $workdir/UPandSP_info.txt $swissprot_database $uniprot_database $workdir/follow_LUT_pipleline_process.txt

echo "Creatred file UPandSP_info" >> $workdir/follow_LUT_pipleline_process.txt


# the following part puts the header to each file in $workdir_AF

python3 $script_directory/extraction_header.py $workdir/human_an_list.txt $workdir/UPandSP_info.txt $workdir_AF/ $workdir/follow_LUT_pipleline_process.txt

echo "Header added to files _complete_residues_AF_PTMs.txt in ${workdir_AF}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF | grep _complete_residues_AF_PTMs.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# the following part is parsing the file with the information extracted from UP and SP and moving them into the
# united file

for element in `ls $workdir_AF | grep _complete_residues_AF_PTMs.txt`
do
  an=$(awk -F'_' '{print $1}' <<< "$element")
  filename="${an}_residues_UPinfos_PTMs_AF.txt"
  if [ ! -f $filename ]
  then
    touch $workdir_AF/$filename
    python3 $script_directory/move_UPandSP_info.py $workdir_AF/$element $workdir/UPandSP_info.txt $workdir_AF/$filename
    rm $workdir_AF/$element
  fi
done
wait

echo "Created files _residues_UPinfos_PTMs_AF.txt in ${workdir_AF}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_AF | grep _residues_UPinfos_PTMs_AF.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt


# this part is creating a parallel database with only the informations extracted from the pdb structures

gunzip $source_human_pdb
name_file1=$(awk -F'.gz' '{print $1}' <<< "$source_human_pdb")
source_human_pdb="${name_file1}"
python3 $script_directory/ceck_human1.py $workdir_PDB/human_pdb.txt $workdir_PDB/human_chains.txt $source_human_pdb
gzip $source_human_pdb
mkdir $workdir_PDB/contacts/
for folder in `ls $source_PDB`
do
  for element in `ls $source_PDB/$folder`
  do
    pdb_code=$(cut -c 1-4 <<< "$element")
    echo $pdb_code >> $workdir_PDB/extraction_pdb_contacts_output.txt
    touch $workdir_PDB/output.txt
    python3 $script_directory/ceck_human2.py $pdb_code $workdir_PDB/human_pdb.txt $workdir_PDB/human_chains.txt $workdir_PDB/output.txt
    exit_status=$?
    if [ $exit_status -eq 1 ]; then
      echo "Not_human" >> $workdir_PDB/extraction_pdb_contacts_output.txt
      continue
    elif [ $exit_status -eq 2 ]; then
      echo "Human" >> $workdir_PDB/extraction_pdb_contacts_output.txt
      python3 /home/pmiglionico/scripts/scripts/PDB_mapping_scripts/pdb2uniprot.py $pdb_code > $workdir_PDB/pdb2uniprot.txt
      python3 $script_directory/extract_contacts_pdb.py $pdb_code $source_PDB/$folder/$element $workdir_PDB/output.txt $workdir_PDB/pdb2uniprot.txt $workdir_PDB/contacts/
      rm $workdir_PDB/output.txt
      rm $workdir_PDB/pdb2uniprot.txt
    else
      echo "Unexpected exit code received!"
      break
    fi
  done
done
wait
for element in `ls -1 $workdir_PDB/contacts`
do
  python3 $script_directory/add_ac_number_pdb.py $workdir_PDB/contacts/$element $workdir/$human_proteome_FASTA
done
wait
rm $workdir_PDB/*
mv $workdir_PDB/contacts/* $workdir_PDB/
rmdir $workdir_PDB/contacts/
wait

echo "Created files_pdb_contacts.txt in ${workdir_PDB}/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir_PDB/ | grep _pdb_contacts.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt
echo "END OF UPDATING OF THE PDB LUT" >> $workdir/follow_LUT_pipleline_process.txt


# this final part is adding to the database the PFAM domais identifyed in each protein of the human proteome

mkdir $workdir_PFAM/domains/
dir_domains="${workdir_PFAM}/domains"
python3 $script_directory/extract_pfam.py $source_HHM $dir_domains
mkdir $workdir_PFAM/fasta/
dir_fasta="${workdir_PFAM}/fasta"
python3 $script_directory/extract_fasta.py $workdir/$human_proteome_FASTA $dir_fasta
mkdir $workdir_PFAM/pairs/
dir_pairs="${workdir_PFAM}/pairs"
python3 $script_directory/extract_pairs.py $source_human_domains $dir_pairs $workdir/human_an_list.txt
for file in `ls $dir_fasta`
do
  prot=$(awk -F'_seq' '{print $1}' <<< "$file")
  name="${prot}_PF00001.txt"
  if [ ! -f $dir_pairs/$name ]
  then
    touch $dir_pairs/$name
    echo "0   0" >> $dir_pairs/$name
  fi
done
wait
source activate /projects/bioinformatics/alphafold
mkdir $workdir_PFAM/database/
for element in `ls $dir_pairs`
do
  echo $element
  protein=$(awk -F'_' '{print $1}' <<< "$element")
  protein_name="${protein}_seq.fasta"
  if [ ! -f $dir_fasta/$protein_name ]
  then
    continue
  fi
  echo $protein_name
  domain=$(awk -F'_|.txt' '{print $2}' <<< "$element")
  domain_name="${domain}_HMM.txt"
  if [ ! -f $dir_domains/$domain_name ]
  then
    echo "${domain}_HMM.txt non trovato!"
  fi
  echo $domain_name
  hmmsearch $dir_domains/$domain_name $dir_fasta/$protein_name >> $workdir/temporary_output.txt
  python3 $script_directory/extract_hmmsearch.py $dir_pairs/$element $workdir/temporary_output.txt $protein $domain $workdir_AF $workdir_PFAM/database
  rm $dir_pairs/$element
  rm $workdir/temporary_output.txt
done
wait
rm $workdir_PFAM/pairs/*
rmdir $workdir_PFAM/pairs/
rm $workdir_PFAM/domains/*
rmdir $workdir_PFAM/domains/
rm $workdir_PFAM/fasta/*
rmdir $workdir_PFAM/fasta/
rm $workdir_PFAM/*
mkdir $workdir/database/
mv $workdir_PFAM/database/* $workdir/database/
rmdir $workdir_PFAM/database/
rm $workdir_AF/*
rmdir $workdir_AF/
rm $workdir/human_an_list.txt
rm $workdir/PTM_output.txt
rm $workdir/UPandSP_info.txt
gzip $workdir/$human_proteome_FASTA
rmdir $workdir_PFAM/
wait

echo "Created files _residues_UPinfos_PFAM_PTMs_AF.txt in ${workdir}/database/ " >> $workdir/follow_LUT_pipleline_process.txt
ls $workdir/database/ | grep _residues_UPinfos_PFAM_PTMs_AF.txt | wc -l  >> $workdir/follow_LUT_pipleline_process.txt
echo "END OF UPDATING OF THE MAIN LUT" >> $workdir/follow_LUT_pipleline_process.txt
echo "end" >> $workdir/follow_LUT_pipleline_process.txt


#COMPLITELY DEBUGGED