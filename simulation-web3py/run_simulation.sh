#!/bin/bash
. <(curl -sLo- "https://git.io/progressbar")
SIMULATION_TIME=60
repetition=1
blockchain=polygon
experiment=polygon_ibft_4
#echo -n -e "Insert the simulation time\n"
#read SIMULATION_TIME
#echo -n -e "Insert the number of repetition\n"
#read repetition
#echo -n -e "Insert the blockchain\n"
#read blockchain
#echo -n -e "Insert the experiment\n"
#read experiment
declare -a lambda=(1)
declare -a functions=(
  #'upload'
  #'another_file_upload'
  #'read'
  #'delete'
  'corrupted_file_check'       #questo lancia la retrieve degli oracoli
  #'read_deny_lost_file_check'
  #'file_check_undeleted_file' #questo lancia la retrieve degli oracoli
)

NUM_LAMBDA=${#lambda[@]}
NUM_FUNCTION=${#functions[@]}

((Max = $NUM_LAMBDA * $NUM_FUNCTION * $repetition))
counter=0
bar::start
for ((idx_lambda = 0; idx_lambda < $NUM_LAMBDA; idx_lambda++)); do

  #eecho -e "\n\nStart simulation with lambda: ${lambda[$idx_lambda]}\n"
  for ((m = 0; m < $NUM_FUNCTION; m++)); do

    #echo -ne " - ${functions[$m]} start                  \r"
    for ((r = 0; r < ${repetition}; r++)); do
      ((counter = counter + 1))
      bar::status_changed $counter $Max
      python3 main.py ${blockchain} ${functions[$m]} -l ${lambda[$idx_lambda]} -t ${SIMULATION_TIME} -s -n ${r} -e ${experiment} 
    done
    #echo -ne " - ${functions[$m]} done                   \r"
    #echo -e "\n"
  done
  #echo -e "\nEnd of simulation with lambda: ${lambda[$idx_lambda]} \n"
done
bar::stop
