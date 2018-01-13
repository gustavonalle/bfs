#!/usr/bin/env python3

import binascii
import hashlib


class Point(object): 
  
   def __init__(self, x, y):
     self.X = x
     self.Y = y
   
   def __eq__(self, other):
     return self.X == other.X and self.Y == other.Y     

   def isInfinity(self):
     return self.X == None and self.Y == None

class PublicKey(object):
    
   def __init__(self, point):
      self.point = point

   def getUncompressed(self):
      pub_key = (self.point.X << 256 | self.point.Y)
      pub_key_bytes = pub_key.to_bytes(64, 'big')
      return b'\x04' + pub_key_bytes

   def getCompressed(self):
      prefix = b'\x02' if self.point.Y & 1 == 0 else b'\x03'
      return prefix + self.point.X.to_bytes(32, 'big')

   # https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses 
   def hash160(self, compressed=True):
      payload =  self.getCompressed() if compressed else self.getUncompressed()
      hash160 = hashlib.new('ripemd160', hashlib.sha256(payload).digest()).digest()
      return hash160

   def __str__(self):
      return f"Public Key: ({hex(self.point.X)}, {hex(self.point.Y)})"

# https://en.wikipedia.org/wiki/Elliptic_curve
class Curve(object):
  
   P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
   G = Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
   
   def hasPoint(self,point):
     return (point.X ** 3 + 7 - point.Y**2) % self.P == 0

   def inv_mod_p(self, x):
     if x % self.P == 0:
        raise ZeroDivisionError("Impossible inverse")
     return pow(x, self.P-2, self.P)

   def sum(self, p, q):
     if(p.isInfinity()): return q
     if(q.isInfinity()): return p
     if not (self.hasPoint(p) and self.hasPoint(q)):
        raise ValueError("Points not part of the curve")
     if(p == q): l = (3 * p.X**2) * self.inv_mod_p(2*p.Y)
     else: l = (q.Y - p.Y) * self.inv_mod_p(q.X - p.X)
     xr = (l**2 - p.X - q.X) % self.P 
     yr = (l*(p.X - xr) - p.Y) % self.P 
     return Point(xr,yr)
   
   def double(self, p):
     return self.sum(p, p)

   def mult(self, p, d):
      n = p
      q = Point(None,None)
      while (d):
        di = d & 1
        if(di == 1): q = self.sum(q, n)
        n = self.double(n) 
        d >>= 1
      return q
  
   def pub_key(self, pk):
      return PublicKey(self.mult(self.G, pk))
