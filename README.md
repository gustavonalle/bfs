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

# Create Hash160 from compressed pub key
hash160 = pub_key.hash160()

# Create Hash160 from uncompressed pub key
hash160 = pub_key.hash160(compressed = False)

print(f"Hash160: {hash160.hex()}")

# Create V1 Address for mainnet
addressv1 = createAddressV1(hash160, AddressType.V1)

# Create V1 Address for testnet
addressv1 = createAddressV1(hash160, AddressType.TESTNET)

print(f"Address (v1): {addressv1}")

```
