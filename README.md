# Bitcoin from scratch 

[![Build Status](https://travis-ci.org/gustavonalle/bfs.svg?branch=master)](https://travis-ci.org/gustavonalle/bfs/)

Simple Python3 Bitcoin library

Currently supported:

* Generate private key
* Genrate pub key - elliptic curve
* Create V1 addresses

## Usage examples:

### Create v1 addresses:

```python
from lib.elliptic import *
from lib.address import *

priv_key = PrivateKey()
print("Private Key: ", priv_key.value())

pub_key = Curve().pub_key(priv_key)
print(pub_key)

# Create Hash160 from compressed pub key
hash160 = pub_key.hash160()

# Create Hash160 from uncompressed pub key
hash160 = pub_key.hash160(compressed = False)

print(f"Hash160: {hash160.hex()}")

# Create V1 Address for main net
addressv1 = AddressV1(hash160, Network.MAIN_NET)

# Create V1 Address for testnet
addressv1 = AddressV1(hash160, Network.TEST_NET)

print(f"Address (v1): {addressv1}")

```
