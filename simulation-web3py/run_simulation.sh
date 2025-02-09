#!/bin/bash

. <(curl -sLo- "https://git.io/progressbar")

SIMULATION_TIME=60
repetition=1
blockchain=polygon
experiment=polygon_ibft_4

declare -a lambda=(1)
declare -a functions=(
  'corrupted_file_check'
  'file_check_undeleted_file'
)

NUM_LAMBDA=${#lambda[@]}
NUM_FUNCTION=${#functions[@]}

((Max = $NUM_LAMBDA * $NUM_FUNCTION * $repetition))
counter=0
first_run=0  # Initialize the first_run flag

echo -n -e "Do you want run the deploy (yes/no)\n"
read VAR
if [ $VAR = "yes" ] || [ $VAR = "y" ] 
    then
        first_run=1
fi

bar::start

for ((idx_lambda = 0; idx_lambda < $NUM_LAMBDA; idx_lambda++)); do
  for ((m = 0; m < $NUM_FUNCTION; m++)); do
    for ((r = 0; r < ${repetition}; r++)); do
      ((counter = counter + 1))
      bar::status_changed $counter $Max

      # Check if this is the first run to include the deploy flag
      deploy_flag=""
      if [ $first_run -eq 1 ]; then
        deploy_flag="-d"
        first_run=0
      fi

      # Execute main.py with the appropriate flags
      python3 main.py ${blockchain} ${functions[$m]} -l ${lambda[$idx_lambda]} -t ${SIMULATION_TIME} -s -n ${r} -e ${experiment} $deploy_flag
    done
  done
done

bar::stop