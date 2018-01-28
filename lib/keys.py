import hashlib
import secrets

from lib import commons
from lib.address import AddressV1, Bech32Address
from lib.elliptic import Curve


class PrivateKey(object):
    MAX_PRIVATE_KEY_VALUE = 1.158 * 10 ** 77
    NBITS = 256
    elliptic = Curve()

    def __init__(self, value=None, compression=True):
        self.compression = compression
        if value is None:
            self.key = self.generate_random(self.NBITS)
        else:
            self.key = value

    @classmethod
    def from_wif(cls, wif):
        start = wif[0]
        compressed = False
        if start == "L" or start == "K" or start == "c" or start == "9":
            compressed = True
        decoded = commons.base58_decode(wif)
        b = decoded.to_bytes(decoded.bit_length() // 8, 'big')
        if compressed:
            b = b[1:-5]
        else:
            b = b[1:-4]
        return PrivateKey(int.from_bytes(b, 'big'), compressed)

    def generate_random(self, nbits):
        key = secrets.randbits(nbits)
        if key < self.MAX_PRIVATE_KEY_VALUE:
            return key
        else:
            return self.generate_random(nbits)

    def create_pub_key(self):
        p = self.elliptic.multiply(self.elliptic.G, self.key)
        return PublicKey(p, self.compression)

    def to_wif(self, network):
        return commons.to_wif(self.key.to_bytes(32, 'big'), network, self.compression)


class PublicKey(object):

    def __init__(self, point, compression=True):
        self.compression = compression
        self.point = point

    def get_value(self):
        if self.compression:
            prefix = b'\x02' if self.point.Y & 1 == 0 else b'\x03'
            return prefix + self.point.X.to_bytes(32, 'big')
        else:
            pub_key = (self.point.X << 256 | self.point.Y)
            pub_key_bytes = pub_key.to_bytes(64, 'big')
            return b'\x04' + pub_key_bytes

    # https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
    def hash160(self):
        payload = self.get_value()
        digest = hashlib.sha256(payload).digest()
        hash160 = hashlib.new('ripemd160', digest).digest()
        return hash160

    def get_address_v1(self, network):
        return AddressV1(self.hash160(), network)

    def get_segwit_address(self, network):
        return Bech32Address.from_hash160(self.hash160(), network)

    def __str__(self):
        return f"({hex(self.point.X)}, {hex(self.point.Y)})"
