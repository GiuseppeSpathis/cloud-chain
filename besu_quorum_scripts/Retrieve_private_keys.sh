
echo -n -e "Insert the folder name\n"
read FOLDER
cd "./config/${FOLDER}"
NUM=`ls -dq *member* | wc -l`
#output file private_key
    private_keys='{"privatekey":[\n'
    for (( c=0; c<$NUM; c++ ))
    do
        
        private_keys="${private_keys} \"0x$(cat './member'$c'/nodekey')\""
        if (($c!=$NUM-1))
        then
            private_keys="${private_keys} \n,"
        fi
    done
    private_keys="${private_keys} ]}"
    echo -e $private_keys>../../src/private_keys.json
echo "Done."