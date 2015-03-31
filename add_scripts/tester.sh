#!/bin/bash 

cd .. 

HOME_DIR=$PWD 
#SCRIPT_DIR=${HOME_DIR}/script

DATA_DIR=${HOME_DIR}/CLASSIC

MGRA_TOOL=${HOME_DIR}/tools/MGRA/build/mgra
PMAG_DIR=${HOME_DIR}/tools/PMAG/
GapAdj_TOOL=${HOME_DIR}/tools/GapAdj/GapAdj
GASTS_TOOL=${HOME_DIR}/tools/GASTS/gasts.jar

## Run MGRA on each dataset and save results in current directory
function run_MGRA {
	echo "START TESTING DATASET"
	for param_folder in ${DATA_DIR}/* 
	do 
		param_folder_name=${param_folder##*/}
		echo MGRA start to work with dataset ${param_folder_name}

		for folder in ${param_folder}/*
		do 
			folder_name=${folder##*/}
			echo Work with ${folder_name}
			${MGRA_TOOL} -c ${folder}/MGRA/sim.cfg -f grimm -g ${folder}/MGRA/blocks.txt -o ${folder}/MGRA/ 2>logerror.txt >/dev/null
		done 		
	done
	echo "END TESTING DATASET"
} 

## Run PMAG+ on each dataset and save results in current directory
function run_PMAG {
	echo "START TESTING DATASET"
	for param_folder in ${DATA_DIR}/* 
	do 
		param_folder_name=${param_folder##*/}
		echo PMAG start to work with dataset ${param_folder_name}

		for folder in ${param_folder}/*
		do 
			folder_name=${folder##*/}
			echo Work with ${folder_name}

			cd ${PMAG_DIR}
			
			cp ${folder}/PMAG/blocks.txt ${PMAG_DIR}/blocks.txt
			cp ${folder}/PMAG/tree.txt ${PMAG_DIR}/tree.txt

			perl RunPMAG+.pl blocks.txt tree.txt result.txt
					
			mv result.txt ${folder}/PMAG/result.txt
			rm tree.txt
			rm blocks.txt 
		done 		
	done
	echo "END TESTING DATASET"
} 

## Run GapAdj on each dataset and save results in current directory
function run_GapAdj {
	echo "START TESTING DATASET"
	for param_folder in ${DATA_DIR}/* 
	do 
		param_folder_name=${param_folder##*/}
		echo GapAdj start to work with dataset ${param_folder_name}

		for folder in ${param_folder}/*
		do 
			folder_name=${folder##*/}
			echo Work with ${folder_name}
			for current_tree_file in ${folder}/GapAdj/*.tree
			do 
				current_tree=${current_tree_file##*/}
				tree_name=${current_tree%.*}
				name_gen=${tree_name}.gap_gen
				echo "Work with ${current_tree} and run on ${name_gen}"
				${GapAdj_TOOL} ${folder}/GapAdj/${current_tree} ${folder}/GapAdj/blocks.txt ${folder}/GapAdj/${name_gen} 25 0.6 2>logerror.txt >/dev/null		
			done
		done 		
	done
	echo "END TESTING DATASET"
} 

## Run GASTS on each dataset and save results in current directory
function run_GASTS {
	echo "START TESTING DATASET"
	for param_folder in ${DATA_DIR}/* 
	do 
		param_folder_name=${param_folder##*/}
		echo "GASTS start to work with dataset ${param_folder_name}"

		for folder in ${param_folder}/*
		do 
			folder_name=${folder##*/}
			echo "Work with ${folder_name}"
			cp -r ${GASTS_TOOL} ${folder}/GASTS/gasts.jar

			java -jar ${folder}/GASTS/gasts.jar ${folder}/GASTS/tree.txt ${folder}/GASTS/blocks.txt 2>logerror.txt

			rm ${folder}/GASTS/gasts.jar 
		done 		
	done
	echo "END TESTING DATASET"
} 

###################
## MAIN FUNCTION ##
###################
if [ "$#" -ne 1 ]; then 
	echo "./tester.sh {1,2,3,4} where 
		1 - run MGRA 
		2 - run PMAG+  
		3 - run GapAdj
		4 - run GASTS
		5 - run InferCarsPro (future)
		6 - run DupCars (future)
		7 - run SCJ (future)"
	exit
fi 

if [ ! -d ${DATA_DIR} ]; then 
	echo "ERROR with ${DATA_DIR}"
	exit 
fi

if [ $1 -eq 1 ]; then 
	echo "Run MGRA"
	run_MGRA
elif [ $1 -eq 2 ]; then 
	echo "Run PMAG"
	run_PMAG
elif [ $1 -eq 3 ]; then 
	echo "Run GapAdj"
	run_GapAdj
elif [ $1 -eq 4 ]; then 
	echo "Run GASTS"
	run_GASTS
elif [ $1 -eq 5 ]; then 
	echo "Run InferCarsPro (future)"
elif [ $1 -eq 6 ]; then 
	echo "Run DupCars (future)"
elif [ $1 -eq 7 ]; then 
	echo "Run SCJ (future)"
fi 

###################
##      END      ##
###################

