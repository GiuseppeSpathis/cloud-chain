#!/bin/bash
echo -n -e "Do you want create the network from zero? (yes/no)\n"
read VAR
declare -a addresses
declare -a node_ids


declare -i NUM_NODES=5


if [ $VAR = "yes" ]
then
    echo -n -e "How many validators you want? (4, 8, 12)\n"
    read num
    if (($num!=4))| (($num != 8))| (($num != 12))
    then
        num=4
    fi
    NUM_NODES=$num
    rm -rf src
    mkdir src
    rm -rf polygon-network
    mkdir polygon-network
    mkdir polygon-network/tmp
    cd polygon-network

    for (( c=1; c<=$NUM_NODES; c++ ))
    do
       ../bin/polygon-edge secrets init --data-dir node-$c >> ./tmp/out$c
    done
    
    for (( c=1; c<=$NUM_NODES; c++ ))
    do
        INPUT=$(cat "./tmp/out$c")
        #Using as delimitator the = then focussing on the important data
        NODE_ID=$(echo $INPUT| cut -d'=' -f 3)
        TMP=$(echo $INPUT| cut -d'=' -f 2)
        ADDRESS=${TMP%N*}
        addresses[$c]=${ADDRESS// /} #removing white-space
        node_ids[$c]=${NODE_ID// /}
    done
    
    ../bin/polygon-edge genesis --consensus ibft --ibft-validators-prefix-path node- --bootnode "/ip4/127.0.0.1/tcp/11001/p2p/${node_ids[1]}" --bootnode "/ip4/127.0.0.1/tcp/12001/p2p/${node_ids[2]}" --premine=${addresses[1]}:1000000000000000000000 --premine=${addresses[2]}:1000000000000000000000 --premine=${addresses[3]}:1000000000000000000000 --premine=${addresses[4]}:1000000000000000000000  --block-gas-limit 16234336 &> /dev/null
    

    #output file private_key
    private_keys='{"privatekey":['
    for (( c=1; c<=$NUM_NODES; c++ ))
        do

            private_keys="${private_keys} \"0x$(cat './node-'$c'/consensus/validator.key')\""
            if (($c!=$NUM_NODES))
            then
            private_keys="${private_keys} ,"
            fi
        done
    private_keys="${private_keys} ]}"
    echo $private_keys>../src/private_keys.json


    
    #output file address
    address='{"address":['
    for (( c=1; c<=$NUM_NODES; c++ ))
        do
            address="${address} \"${addresses[$c]}\""
            if (($c!=$NUM_NODES))
            then
            address="${address} ,"
            fi
        done
    address="${address} ]}"
    echo $address>../src/address.json
    rm -rf tmp
    echo -e "Network initialized correctly\n"


    for (( c=1; c<=$NUM_NODES; c++ ))
        do
            rm -rf ./tmp/out$c
        done
else
    cd polygon-network
fi

    for (( c=1; c<=$NUM_NODES; c++ ))
        do
            tmp=$((c+10))
            command_run="${command_run} ../bin/polygon-edge server --data-dir ./node-${c} --chain genesis.json --grpc :${tmp}000 --libp2p :${tmp}001 --jsonrpc :${tmp}002 --seal &"
            if (($c==$NUM_NODES))
            then
            command_run="${command_run} ../bin/polygon-edge server --chain genesis.json --dev --log-level debug"
            fi
        done
   

echo -n -e "Do you want run the newtork (yes/no)\n"
read VAR
if [ $VAR = "yes" ]
then
   eval $command_run
fi