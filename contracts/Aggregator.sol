// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
pragma experimental ABIEncoderV2;

import "./FileDigestOracle.sol";

contract Aggregator {

    struct OracleInfo {
        FileDigestOracle oracle;
        uint256 reputation;
    }

    OracleInfo[] private oracles;

    constructor(address[] memory _oracles) {
        for (uint256 i = 0; i < _oracles.length; i++) {
            oracles.push(OracleInfo({
                oracle: FileDigestOracle(_oracles[i]),
                reputation: 100
            }));
        }
    }

    function DigestRequest(string calldata url) public {
        for (uint256 i = 0; i < oracles.length; i++) {
            if (oracles[i].reputation >= 50) {
                oracles[i].oracle.DigestRequest(url);
            }
        }
    }

    function DigestStore(string calldata url, bytes32 digest) public {
        for (uint256 i = 0; i < oracles.length; i++) {
            if (oracles[i].reputation >= 50) {
                oracles[i].oracle.DigestStore(url, digest);
            }
        }
    }

    // Funzione che recupera tutti i digest, li ordina e restituisce la mediana
    function DigestRetrieve(string calldata url, bool fileIsImportant) public returns (bytes32) {
        uint256 n = oracles.length;
        require(n > 0, "Nessun oracle disponibile");

        // Conta gli oracoli validi (reputazione >= 50)
        uint256 validCount = 0;
        for (uint256 i = 0; i < n; i++) {
            if (oracles[i].reputation >= 50) {
                validCount++;
            }
        }
        require(validCount > 0, "Nessun oracle valido");


        // Recupera i digest dagli oracle validi
        bytes32[] memory digests = new bytes32[](validCount);
        uint256 j = 0;
        for (uint256 i = 0; i < n; i++) {
            if (oracles[i].reputation >= 50) {
                digests[j] = oracles[i].oracle.DigestRetrieve(url,fileIsImportant);
                j++;
            }
        }

        // Ordina l'array dei digest
        quickSort(digests, 0, int(validCount  - 1));

        // Calcola la mediana: se il numero è pari si usa l'elemento in posizione validCount/2
        bytes32 median = digests[validCount / 2];
        // Aggiorna la reputazione di ogni oracolo
        for (uint256 i = 0; i < n; i++) {
            bytes32 digest = oracles[i].oracle.DigestRetrieve(url, fileIsImportant);
            if (digest == median) {
                oracles[i].reputation += 10;
            } else {
                if (oracles[i].reputation >= 10) {
                    oracles[i].reputation -= 10;
                }
            }
        }
        return median;
    }

    // Algoritmo quickSort corretto per array di bytes32 in memoria.
    function quickSort(bytes32[] memory arr, int left, int right) internal pure {
        int i = left;
        int j = right;
        if (i >= j) return;

        // Calcola il pivot: nota la conversione da int a uint per l'indicizzazione
        bytes32 pivot = arr[uint(left + (right - left) / 2)];
        while (i <= j) {
            while (i <= right && arr[uint(i)] < pivot) i++;
            while (j >= left && pivot < arr[uint(j)]) j--;
            if (i <= j) {
                (arr[uint(i)], arr[uint(j)]) = (arr[uint(j)], arr[uint(i)]);
                i++;
                j--;
            }
        }
        if (left < j)
            quickSort(arr, left, j);
        if (i < right)
            quickSort(arr, i, right);
    }


    // Restituisce gli indirizzi e la reputazione di ogni oracle
    function getOraclesInfo() public view returns (address[] memory, uint256[] memory, bool[] memory) {
        uint256 len = oracles.length;
        address[] memory addrs = new address[](len);
        uint256[] memory reputations = new uint256[](len);
        bool[] memory maliciousFlags = new bool[](len);
        for (uint256 i = 0; i < len; i++) {
            addrs[i] = address(oracles[i].oracle);
            reputations[i] = oracles[i].reputation;
            maliciousFlags[i] = oracles[i].oracle.malicious();
        }
        return (addrs, reputations, maliciousFlags);
    }

    
}