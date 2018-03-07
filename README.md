# Bitcoin from scratch 

[![Build Status](https://travis-ci.org/gustavonalle/bfs.svg?branch=master)](https://travis-ci.org/gustavonalle/bfs/)

Pure Python3 Bitcoin library

Currently Bitcoin features supported:

* Generate private key
* Generate pub key - elliptic curve
* Create V1 and bech32 addresses for Testnet and Mainnet
* Create offline signed transactions
* Spend transactions with multiple inputs (P2PKH/P2PK/P2WPKH/P2SH-P2WPKH) and outputs (P2PKH/P2PK/P2WPKH)
* RFC-6979 for deterministic ECDSA signature

Hard forks supported:

* [B2X](https://b2x-segwit.io)
* [BTN](http://btn.kim) 


## Usage examples:

Run  ```jupyter notebook examples.ipynb``` 
