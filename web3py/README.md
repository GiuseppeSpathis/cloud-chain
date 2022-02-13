# cloud-chain

## Blockchain informations

| Blokchain | Consensus mechanisms        | Validator nodes | Interarrival time Poisson (λ) |
| :--- |:----------------------------| :--- | :--- |
| GoQuorum | IBFT, IBFT2.0, QBFT, Clique | 4, 8, 12 | 2, 1, 1/2, 1/5, 1/10 |
| Hyperledger Besu | IBFT, IBFT2.0, QBFT, Clique | 4, 8, 12 | 2, 1, 1/2, 1/5, 1/10 |
| Polygon | IBFT (PoA), IBFT (PoS)      | 4, 8, 12 | 2, 1, 1/2, 1/5, 1/10 |

## Test configurations

| ID | poly - besu - goqu                    | Validator nodes | Interarrival time Poisson (λ) |
| :--- |:--------------------------------------| :--- | :--- |
| 1 | IBFT (PoA) vs IBFT vs IBFT            | 4, 8, 12 | 2, 1, 1/2, 1/5, 1/10 |
| 2 | IBFT (PoA) vs IBFT2.0 vs IBFT2.0      | 4, 8, 12 | 2, 1, 1/2, 1/5, 1/10 |
| 3 | IBFT (PoA) vs QBFT vs QBFT                  | 4, 8, 12 | 2, 1, 1/2, 1/5, 1/10 |
| 4 | IBFT (PoA) vs Clique vs Clique              | 4, 8, 12 | 2, 1, 1/2, 1/5, 1/10 |
| 5 | IBFT (PoS) vs IBFT2.0 vs IBFT2.0      | 4, 8, 12 | 2, 1, 1/2, 1/5, 1/10 |

### Fixed values
- Gas limit: 0xf7b760 (?)
- Block period seconds: 5 (?)

## Parameters to measure

- Service time -> response time
  - mean, min, max, median
- Is busy -> use of blockchain
  - mean, min, max, median
- ...
- Is there a transient? (parallel requests)
