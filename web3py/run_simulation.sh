#!/bin/bash
SIMULATION_TIME=1
declare -a lambda=(2 1 0.5 0.2 0.1)
declare -a functions=('cloud_sla_creation_activation'
            'upload'
            'read'
            'delete'
            'file_check_undeleted_file'
            'another_file_upload'
            'read_deny_lost_file_check'
            'another_file_upload_read'
            'corrupted_file_check')

for (( c=0; c<=4; c++ ))
do
    for ((m=0; m<=8; m++ ))
    do
        echo ${functions[$m]}
        python main.py polygon ${functions[$m]} -l ${lambda[$c]} -t ${SIMULATION_TIME}
    done
done