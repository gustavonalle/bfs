# Bitcoin from scratch 

Simple Python3 Bitcoin library

Currently supported:

* Generate private key
* Genrate pub key - elliptic curve
* Create V1 addresses

Usage:

```
$ python3 -i bitcoin.py

priv_key = generate_random(256)
print("Private Key: ", hex(priv_key))

pub_key = Curve().pub_key(priv_key)
print(pub_key)

hash160 = pub_key.hash160()
print(f"Hash160: {hash160.hex()}")

addressv1 = createAddressV1(hash160, AddressType.V1)
print(f"Address (v1) mainNet: {addressv1}")

```
