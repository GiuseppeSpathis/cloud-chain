#!/bin/bash
. <(curl -sLo- "https://git.io/progressbar")
SIMULATION_TIME=60
repetition=10
blockchain=polygon
echo -n -e "Insert the simulation time\n"
read SIMULATION_TIME
echo -n -e "Insert the number of repetition\n"
read repetition
echo -n -e "Insert the blockchain\n"
read blockchain
declare -a lambda=(2 1 0.5)
declare -a functions=(
  #'read'
  'upload'
  #'delete'
  #'another_file_upload'
  #'another_file_upload_read'
  #'file_check_undeleted_file'
  #'read_deny_lost_file_check'
  #'cloud_sla_creation_activation'
  #'corrupted_file_check'
)

((Max = 3 * 1 * $repetition))
counter=0
bar::start
for ((idx_lambda = 0; idx_lambda < 3; idx_lambda++)); do

  echo -e "\n\nStart simulation with lambda: ${lambda[$idx_lambda]}\n"
  for ((m = 0; m <= 1; m++)); do

    echo -ne " - ${functions[$m]} start                  \r"
    for ((r = 0; r < ${repetition}; r++)); do
      ((counter = counter + 1))
      bar::status_changed $counter $Max
      python main.py ${blockchain} ${functions[$m]} -l ${lambda[$idx_lambda]} -t ${SIMULATION_TIME} -s -n ${r} -e besu_qbft_4 &>/dev/null
    done
    echo -ne " - ${functions[$m]} done                   \r"
    echo -e "\n"
  done
  echo -e "\nEnd of simulation with lambda: ${lambda[$idx_lambda]} \n"
done
bar::stop
