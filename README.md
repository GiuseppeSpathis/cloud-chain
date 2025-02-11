# Project Overview
This project extends the cloud-chain system developed by AnaNSi-research, which implemented a set of SLA contracts between a cloud provider and a client on the blockchain. In the original project, only a single oracle was used to obtain file path related to digests to monitor potential SLA violations. My extension introduces a decentralized oracle system, comprising five oracles per SLA contract and an aggregator that collects the responses, computes the median, and updates the reputation of each oracle accordingly. Each oracle is initially assigned a reputation of 100. When the aggregator processes a request from the SLA contract to retrieve digests from the oracle contracts, it calculates the median of the responses and increases an oracle’s reputation by 10 if its response matches the median; otherwise, it decreases the reputation by 10. Should an oracle’s reputation fall below 50, it is deemed unreliable and is no longer queried for the median calculation. Moreover, the system accounts for the possibility of malicious oracles: these typically return correct digests to accumulate reputation, but when confronted with a request for an important file, they deliberately return an incorrect digest. Despite their misbehavior, their high reputation may cause the aggregator to continue trusting them.

# Running the Simulation
To run the simulation, you must first launch a local Polygon blockchain. This is achieved by executing the script run_polygon.sh and by following the instructions:

- Do you want create the network from zero?
yes
- How many validators do you want?
4
- Which consensus mechanism do you want to use?
1
- Do you want run the newtork?
yes

Once the network is running, open another terminal and launch the simulation using the script run_simulation.sh, responding affirmatively when prompted to deploy the contracts. This configuration prepares the system to execute the selected functions on the blockchain as defined in the setup.

# Implementation Details
The oracles are deployed via the init_contracts function in the web3client.py file, specifically in the __deploy_contract routine, where there is a 30% chance that an oracle will be designated as malicious. This attribute is stored in a boolean field within the FileDigestOracle contract. Furthermore, in the DigestRetrieve function, if an oracle is malicious and the request pertains to an important file, the digest returned is intentionally altered (for instance, the last three bytes are set to a fixed value such as 0xABCDEF), thereby providing an incorrect response. The run_simulation.sh script allows the user to choose which functions to execute on the blockchain; available options include "corrupted_file_check" and "file_check_undeleted_file", which are applied respectively to important files and to files of lesser importance with regard to malicious oracle behavior. The variable NUM_TRANSACTIONS, defined in settings.py, determines the number of times each function will be executed in the simulation.

# Future Work
Future work could focus on determining the threshold number of malicious oracles beyond which the decentralized oracle system becomes unreliable. In addition, alternative approaches for achieving consensus among decentralized oracles could be explored, potentially eliminating the need for an aggregator.






