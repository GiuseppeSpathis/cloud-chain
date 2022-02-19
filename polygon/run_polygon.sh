#!/bin/bash
echo -n -e "Do you want create the network from zero? (yes/no)\n"
read VAR
declare -a addresses
declare -a node_ids


declare -i NUM_NODES=4


if [ $VAR = "yes" ]
then
    
    
    
    
    echo -n -e "\nHow many validators do you want? (4, 8, 12)\n"
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
    cd ..
    
    
    echo -n -e "\nWhich consensus mechanism do you want to use? (1-IBFT, 2-PoS)\n"
    read mechanism

    if (($mechanism==1))
    then
        mechanism='--consensus ibft'
    elif (($mechanism==2))
    then
        mechanism='--pos'
        if [ -d "./staking-contracts/" ]
        then
            
            #git clone https://github.com/0xPolygon/staking-contracts.git &> /dev/null
            cd staking-contracts
            echo Installing node modules...
            #npm i &> /dev/null
            echo building contract...
            npm run build &> /dev/null
            private_keys=''
            for (( c=1; c<=$NUM_NODES; c++ ))
            do
                private_keys="${private_keys} 0x$(cat '../polygon-network/node-'$c'/consensus/validator.key')"
                
                if (($c!=$NUM_NODES))
                then
                    private_keys="${private_keys} ,"
                fi
            done
            echo -e "JSONRPC_URL=http://127.0.0.1:8545\nPRIVATE_KEYS=${private_keys}\nSTAKING_CONTRACT_ADDRESS=0x0000000000000000000000000000000000001001">.env
            cd ..
        fi
    else
        mechanism='--consensus ibft'
    fi
    cd polygon-network
    
    if [[ $mechanism == "--pos" ]]
    then
        epoch="--epoch-size 50"
        deploy_pos="& cd ../staking-contracts ; npm run deploy --silent ;npm run stack --silent; echo finish stacking-------------------------------"
    else
        epoch=''
        deploy_pos=""
    fi
    ../bin/polygon-edge genesis --consensus ibft ${mechanism} ${epoch} --ibft-validators-prefix-path node- --bootnode "/ip4/127.0.0.1/tcp/11001/p2p/${node_ids[1]}" --bootnode "/ip4/127.0.0.1/tcp/12001/p2p/${node_ids[2]}" --premine=${addresses[1]}:1000000000000000000000 --premine=${addresses[2]}:1000000000000000000000 --premine=${addresses[3]}:1000000000000000000000 --premine=${addresses[4]}:1000000000000000000000  --block-gas-limit 16234336 &> /dev/null
    
    
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
    tmp=$((c+9))
    command_run="${command_run} ../bin/polygon-edge server --data-dir ./node-${c} --chain genesis.json --grpc :${tmp}000 --libp2p :${tmp}001 --jsonrpc :${tmp}002 --seal &"
    if (($c==$NUM_NODES))
    then
        command_run="${command_run} ../bin/polygon-edge server --chain genesis.json --dev --log-level debug "
    fi
done


echo -n -e "Do you want run the newtork (yes/no)\n"
read VAR
if [ $VAR = "yes" ]
then
    eval $command_run
fi
