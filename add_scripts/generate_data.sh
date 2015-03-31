#!/bin/bash

HOME_DIR=${PWD}
NAME_DIR=${HOME_DIR}/CLASSIC
TOOL_NAME=${HOME_DIR}/shiva

#######################################
## Parameters for generated datasets ##
#######################################
#>Parameters file

NUMBERGENE=(200 300 400)
NUMBERGENOMES=(6 9 12 15)
NUMBERCHR=5

PERBRANCH=(100 200)
VARIANCE=(50 100)

INVERSION=0.9
TRANSPOSITION=0.0
TRANSVERSION=0.0
FISSION=0.0
FUSSION=0.0
TRANSLOCATION=0.1

DELETION=0
LENGTH_DEL=0
INSERTION=0
LENGTH_INS=0

NUMBER_DATASETS=10

## Function for generation datasets with parameters ##
function build_datasets { 
	for numb_genome in ${NUMBERGENOMES[@]}
	do
		for numb_gene in ${NUMBERGENE[@]}
		do 
			for per_branch in ${PERBRANCH[@]}
			do 
				echo New dataset: ${numb_genome} ${numb_gene} ${per_branch}
				name_dir=${numb_genome}_${numb_gene}_${per_branch}_0
				current_dir=${NAME_DIR}/${name_dir}
				mkdir ${current_dir}
				for i in {1..10}
				do 
					echo Dataset ${i}
					mkdir ${current_dir}/${i}

					## Save configuration file ##
					echo ">Parameters file" > ${current_dir}/${i}/config.txt
					echo >> ${current_dir}/${i}/config.txt

					echo ${numb_gene} >> ${current_dir}/${i}/config.txt 
					echo ${numb_genome} >> ${current_dir}/${i}/config.txt 
					echo ${NUMBERCHR} >> ${current_dir}/${i}/config.txt
					echo >> ${current_dir}/${i}/config.txt

					variation=$(( per_branch / 2 ))
					echo ${per_branch} >> ${current_dir}/${i}/config.txt
					echo ${variation} >> ${current_dir}/${i}/config.txt
					echo >> ${current_dir}/${i}/config.txt

					echo ${INVERSION} >> ${current_dir}/${i}/config.txt
					echo ${TRANSPOSITION} >> ${current_dir}/${i}/config.txt
					echo ${TRANSVERSION} >> ${current_dir}/${i}/config.txt
					echo ${FISSION} >> ${current_dir}/${i}/config.txt
					echo ${FUSSION} >> ${current_dir}/${i}/config.txt
					echo ${TRANSLOCATION} >> ${current_dir}/${i}/config.txt

					echo ${DELETION} >> ${current_dir}/${i}/config.txt
					echo ${LENGTH_DEL} >> ${current_dir}/${i}/config.txt
					echo ${INSERTION} >> ${current_dir}/${i}/config.txt
					echo ${LENGTH_INS} >> ${current_dir}/${i}/config.txt

					## run shiva ##
					cp ${TOOL_NAME} ${current_dir}/${i}/shiva

					cd ${current_dir}/${i}
					./shiva config.txt blocks.txt bad_tree.txt ancestral.txt tree.txt >log.txt
					rm shiva
					cd ${HOME_DIR}
					
				done 
			done 
		done 
	done
}

##########
## Main ##
##########
if [ -d ${NAME_DIR} ]; then 
	rm -rf ${NAME_DIR} 
fi 

mkdir ${NAME_DIR}

build_datasets

##########
##  END ##
##########




