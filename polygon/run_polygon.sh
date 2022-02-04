#! /bin/bash
echo -n -e "Do you want create the network from zero? (yes/no)\n"
read VAR
declare -a addresses
declare -a node_ids


if [ $VAR = "yes" ]
then
    rm -rf src
    mkdir src
    rm -rf polygon-network
    mkdir polygon-network
    mkdir polygon-network/tmp
    cd polygon-network
    for i in 1 2 3 4
    do
       ../bin/polygon-sdk secrets init --data-dir node-$i >> ./tmp/out$i
    done
    
    for i in 1 2 3 4
    do
        INPUT=$(cat "./tmp/out$i")
        #Using as delimitator the = then focussing on the important data
        NODE_ID=$(echo $INPUT| cut -d'=' -f 3)
        TMP=$(echo $INPUT| cut -d'=' -f 2)
        ADDRESS=${TMP%N*}
        addresses[$i]=${ADDRESS// /} #removing white-space
        node_ids[$i]=${NODE_ID// /}
    done
    
    ../bin/polygon-sdk genesis --consensus ibft --ibft-validators-prefix-path test-chain- --bootnode "/ip4/127.0.0.1/tcp/10001/p2p/${node_ids[1]}" --bootnode "/ip4/127.0.0.1/tcp/20001/p2p/${node_ids[2]}" --premine=${addresses[1]}:1000000000000000000000 --premine=${addresses[2]}:1000000000000000000000 --premine=${addresses[3]}:1000000000000000000000 --premine=${addresses[4]}:1000000000000000000000 &> /dev/null
    

    #output file private_key
    private_keys='{"privatekey":['
    for i in 1 2 3 4
        do

            private_keys="${private_keys} \"0x$(cat './node-'$i'/consensus/validator.key')\""
            if (($i!=4))
            then
            private_keys="${private_keys} ,"
            fi
        done
    private_keys="${private_keys} ]}"
    echo $private_keys>../src/private_keys.json


    
    #output file address
    address='{"address":['
    for i in 1 2 3 4
        do
            address="${address} \"${addresses[$i]}\""
            if (($i!=4))
            then
            address="${address} ,"
            fi
        done
    address="${address} ]}"
    echo $address>../src/address.json
    rm -rf tmp
    echo -e "Network initialized correctly\n"


    for i in 1 2 3 4
        do
            rm -rf ./tmp/out$i
        done
else
    cd polygon-network
fi



echo -n -e "Do you want run the newtork (yes/no)\n"
read VAR
if [ $VAR = "yes" ]
then
    
    ../bin/polygon-sdk server --data-dir ./test-chain-1 --chain genesis.json --grpc :10000 --libp2p :10001 --jsonrpc :10002 --seal &
    ../bin/polygon-sdk server --data-dir ./test-chain-2 --chain genesis.json --grpc :20000 --libp2p :20001 --jsonrpc :20002 --seal &
    ../bin/polygon-sdk server --data-dir ./test-chain-3 --chain genesis.json --grpc :30000 --libp2p :30001 --jsonrpc :30002 --seal &
    ../bin/polygon-sdk server --data-dir ./test-chain-4 --chain genesis.json --grpc :40000 --libp2p :40001 --jsonrpc :40002 --seal &
    ../bin/polygon-sdk server --chain genesis.json --dev --log-level debug
fi

