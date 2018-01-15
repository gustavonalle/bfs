import hashlib
import hmac
import math

from lib.utils import Encoder


class Point(object):

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def is_infinity(self):
        return self.X is None and self.Y is None


class PublicKey(object):

    def __init__(self, point):
        self.point = point

    def get_uncompressed(self):
        pub_key = (self.point.X << 256 | self.point.Y)
        pub_key_bytes = pub_key.to_bytes(64, 'big')
        return b'\x04' + pub_key_bytes

    def get_compressed(self):
        prefix = b'\x02' if self.point.Y & 1 == 0 else b'\x03'
        return prefix + self.point.X.to_bytes(32, 'big')

    # https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
    def hash160(self, compressed=True):
        payload = self.get_compressed() if compressed else self.get_uncompressed()
        digest = hashlib.sha256(payload).digest()
        hash160 = hashlib.new('ripemd160', digest).digest()
        return hash160

    def __str__(self):
        return f"Public Key: ({hex(self.point.X)}, {hex(self.point.Y)})"


class SigHash(object):
    ALL = b'\x01'


# https://en.wikipedia.org/wiki/Elliptic_curve
class Curve(object):
    secp256k1_p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
    G = Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
              0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    h = 0x01

    def __init__(self, p=secp256k1_p):
        self.p = p
        self.qlen = p.bit_length()

    def has_point(self, point):
        return (point.X ** 3 + 7 - point.Y ** 2) % self.p == 0

    def inv_mod_p(self, x):
        if x % self.p == 0:
            raise ZeroDivisionError("Impossible inverse")
        return pow(x, self.p - 2, self.p)

    def inv_mod_n(self, x):
        if x % self.n == 0:
            raise ZeroDivisionError("Impossible inverse")
        return pow(x, self.n - 2, self.n)

    def sum(self, p, q):
        if p.is_infinity():
            return q
        if q.is_infinity():
            return p
        if not (self.has_point(p) and self.has_point(q)):
            raise ValueError("Points not part of the curve")
        if p == q:
            delta = (3 * p.X ** 2) * self.inv_mod_p(2 * p.Y)
        else:
            delta = (q.Y - p.Y) * self.inv_mod_p(q.X - p.X)
        xr = (delta ** 2 - p.X - q.X) % self.p
        yr = (delta * (p.X - xr) - p.Y) % self.p
        return Point(xr, yr)

    def double(self, p):
        return self.sum(p, p)

    def multiply(self, p, d):
        n = p
        q = Point(None, None)
        while d:
            di = d & 1
            if di == 1:
                q = self.sum(q, n)
            n = self.double(n)
            d >>= 1
        return q

    def pub_key(self, pk):
        return PublicKey(self.multiply(self.G, pk))

    def int2octets(self, num):
        rlen = math.ceil(self.qlen / 8)
        return num.to_bytes(rlen, 'big')

    def bits2int(self, b):
        v = int.from_bytes(b, 'big')
        vlen = len(b) * 8
        if vlen > self.qlen:
            v = v >> (vlen - self.qlen)
        return v

    def bits2octets(self, b):
        z1 = self.bits2int(b)
        z2 = z1 % self.p
        return self.int2octets(z2)

    def generate_r(self, pk, message):
        # step a
        x = self.int2octets(pk)
        h1 = self.bits2octets(hashlib.sha256(message).digest())
        vlen = 32
        # step b
        v = b'\x01' * vlen

        # step c
        k = b'\x00' * vlen

        # step d
        k = hmac.new(k, v + b'\x00' + x + h1, digestmod=hashlib.sha256).digest()

        # step e
        v = hmac.new(k, v, digestmod=hashlib.sha256).digest()

        # step f
        k = hmac.new(k, v + b'\x01' + x + h1, digestmod=hashlib.sha256).digest()

        # step g
        v = hmac.new(k, v, digestmod=hashlib.sha256).digest()

        # step h
        while True:
            t = b''
            while len(t) < (self.qlen + 7) / 8:
                v = hmac.new(k, v, digestmod=hashlib.sha256).digest()
                t += v
            kc = self.bits2int(t)
            if 0 < kc < self.p:
                return kc
            k = hmac.new(k, v + b'\x00', digestmod=hashlib.sha256).digest()
            v = hmac.new(k, v, digestmod=hashlib.sha256).digest()

    def ecdsa(self, private_key, payload):
        k = self.generate_r(private_key, payload)
        p = self.pub_key(k)
        r = p.point.X
        h = hashlib.sha256(payload).digest()
        hm = int.from_bytes(h, 'big') % self.n
        s = self.inv_mod_n(k) * (hm + private_key * r) % self.n
        if s > self.n / 2:
            s = -1 * s % self.n
        return r, s

    def sign(self, message, private_key, sig_hash):
        ecdsa = self.ecdsa(private_key, message)
        return Encoder.der(ecdsa, sig_hash)
