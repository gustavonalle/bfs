# Bitcoin from scratch 

[![Build Status](https://travis-ci.org/gustavonalle/bfs.svg?branch=master)](https://travis-ci.org/gustavonalle/bfs/)

Pure Python3 Bitcoin library

Currently supported:

* Generate private key
* Genrate pub key - elliptic curve
* Create V1 addresses

## Usage examples:

### Create v1 addresses:

```python
from lib.elliptic import *
from lib.address import *

# Create a random compressed private key
priv_key = PrivateKey()
print("Private Key: ", priv_key.value())

pub_key = Curve().pub_key(priv_key)
print(pub_key)

# Create Hash160 from compressed pub key
hash160 = pub_key.hash160()
print(f"Hash160: {hash160.hex()}")

# Create V1 Address for main net
addressv1 = AddressV1(hash160, Network.MAIN_NET)

# Create V1 Address for testnet
addressv1 = AddressV1(hash160, Network.TEST_NET)

print(f"Address (v1): {addressv1}")

```

### Spend P2PKH output:

```python
from lib.keys import PrivateKey
from lib.spender import Spender, Utxo, Destination
private_key = PrivateKey(0x111111)

spender = Spender()

# Specify tx_hash, index, address and amount unspent from the UTXO:
utxo = Utxo("fedcf6dfb752deadbb5f5407538e0dfec0c3e14927c3b46592811ba584fabd11", 
            1,
            "msAP1h4Bv9mar7hSXM9d27adwHeuvotixB", 
            1.21716322)

# Create one or more outputs
# Send 1 BTC to mzDUHce6H8RAyXW8GCioV8UtiYyvA3mEqE
send_to = Destination(1.00000000, "mzDUHce6H8RAyXW8GCioV8UtiYyvA3mEqE")

# Send the rest (minus a 20000 satoshi fee) to the same address from the UTXO
change = Destination(1.21716322 - 1 - 0.0002, "msAP1h4Bv9mar7hSXM9d27adwHeuvotixB")

spender.add_utxos(utxo)
spender.add_destinations(send_to, change)

# Create a signed transaction to spend the UTXO
spend_tx = spender.create_p2pkh_tx(private_key)

# Serialized transaction ready to be broadcast
print(spend_tx.hex())



```