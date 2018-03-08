from lib import bech32
from lib.bech32 import *
from lib.commons import *


class AddressV1(object):

    def __init__(self, hash160, network):
        self.hash160 = hash160
        self.network = network
        self.value = self.create(hash160, network)

    # https://en.bitcoin.it/wiki/Base58Check_encoding
    @staticmethod
    def create(hash160, address_type):
        return AddressV1.create_with_prefix(hash160, address_type.value)

    def create_with_prefix(hash160, prefix):
        step1 = prefix + hash160
        step2 = double_sha256(step1)
        step3 = step2[0:4]
        step4 = step1 + step3
        return base58_encode(step4)

    def __str__(self):
        return self.value


# https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
class Bech32Address(object):
    witver = 0

    def __init__(self, hash160, address, network):
        self.hash160 = hash160
        self.network = network
        self.address = address
        if self.network == Network.MAIN_NET:
            self.hrp = "bc"
        else:
            self.hrp = "tb"
        self.value = encode(self.hrp, 0, list(hash160))

    @classmethod
    def from_address(cls, address):
        hrp = address[0:2]
        network = None
        if hrp == "bc":
            network = Network.MAIN_NET
        if hrp == "tb":
            network = Network.TEST_NET
        if network is None:
            raise RuntimeError("Unknown hrp in bech32 address")
        hrp, data = bech32.decode(hrp, address)
        hash160 = bytes(data)
        return cls(hash160, address, network)

    @classmethod
    def from_hash160(cls, hash160, network):
        hrp = None
        if network.name == 'TEST_NET':
            hrp = "tb"
        if network.name == 'MAIN_NET':
            hrp = "bc"

        address = bech32.encode(hrp, cls.witver, list(hash160))
        return cls(hash160, address, network)

    def __str__(self):
        return self.value
