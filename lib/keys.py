import hashlib
import secrets


class PrivateKey(object):
    MAX_PRIVATE_KEY_VALUE = 1.158 * 10 ** 77
    NBITS = 256

    def __init__(self, value=None):
        if value is None:
            self.key = self.generate_random(self.NBITS)
        else:
            self.key = value

    def generate_random(self, nbits):
        key = secrets.randbits(nbits)
        if key < self.MAX_PRIVATE_KEY_VALUE:
            return key
        else:
            return self.generate_random(nbits)

    def value(self):
        return self.key

    def __str__(self):
        return f"Private Key: {hex(self.key)}"


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
