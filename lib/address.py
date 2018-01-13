#!/usr/bin/env python3

import binascii
import hashlib
import itertools
import secrets
from enum import Enum

class AddressType(Enum):
     V1 = b'\x00'
     P2SH     = b'\x05'
     TESTNET  = b'\x6f'
     
MAX_PRIV_KEY_VALUE = 1.158 * 10**77

# https://en.bitcoin.it/wiki/Base58Check_encoding
def createAddressV1(n, addressType):
   step1 = addressType.value + n
   step2 = doubleSHA256(step1)
   step3 = step2[0:4]
   step4 = step1 + step3
   return base58_encode(step4)

def base58_encode(b):   
   digits = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
   payload = int.from_bytes(b, 'big') 
   res = ''
   while(payload > 0):
     (payload, r) = divmod(payload, 58)
     res += digits[r]
   for item in itertools.takewhile(lambda x: x == 0, b):
      res += digits[0]
   return res[::-1]
  
def doubleSHA256(b):
   return hashlib.sha256(hashlib.sha256(b).digest()).digest() 
   

def generate_random(nbits):  
    key = secrets.randbits(nbits)
    if(key < MAX_PRIV_KEY_VALUE): return key
    else: return generate_random(nbits)
