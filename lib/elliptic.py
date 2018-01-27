import hashlib
import hmac
import math


class Point(object):

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def is_infinity(self):
        return self.X is None and self.Y is None


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
        if p.X == q.X and p.Y != q.Y:
            return Point(None, None)
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

    def multiply_g(self, pk):
        return self.multiply(self.G, pk)

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

    def generate_r(self, pk_value, message):
        # step a
        x = self.int2octets(pk_value)
        h1 = self.bits2octets(message)
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

    def ecdsa(self, private_key_value, pub_key_point, payload):
        k = self.generate_r(private_key_value, payload)
        p = self.multiply_g(k)
        r = p.X
        hm = int.from_bytes(payload, 'big') % self.n
        s = self.inv_mod_n(k) * (hm + private_key_value * r) % self.n
        if s > self.n / 2:
            s = -1 * s % self.n
        return r, s
