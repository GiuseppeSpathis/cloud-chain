#!/bin/bash
. <(curl -sLo- "https://git.io/progressbar")
echo -n -e "Insert the simulation time\n"
#read SIMULATION_TIME
SIMULATION_TIME=2
echo -n -e "Insert the number of repetition\n"
#read repetition
repetition=2
declare -a lambda=(2 1 0.5 0.2 0.1)
declare -a functions=(
    'read'
    'upload'
    'delete'
    'another_file_upload'
    'another_file_upload_read'
    'file_check_undeleted_file'
    'read_deny_lost_file_check'
    'cloud_sla_creation_activation'
'corrupted_file_check')

((Max=5*9*$repetition))
counter=0
bar::start
for (( lambdaidx=0; lambdaidx<5; lambdaidx++ ))
do
    
    echo -e "lambda ${lambda[$lambdaidx]}\n"
    for ((m=0; m<=8; m++ ))
    do
        
        echo -ne "${functions[$m]} start                  \r"
        for (( r=0; r<${repetition}; r++ ))
        do
            ((counter=counter+1))
            bar::status_changed $counter $Max
            #sleep 0.1
            python main.py polygon ${functions[$m]} -l ${lambda[$lambdaidx]} -t ${SIMULATION_TIME} -s -n ${r} 
        done
        echo -ne "${functions[$m]} done                  \r"
        #sleep 0.09
    done
    echo -e "\n Done \n"
done
bar::stop
