from lib.commons import *


class AddressV1(object):

    def __init__(self, hash160, network):
        self.hash160 = hash160
        self.network = network
        self.value = self.create(hash160, network)

    # https://en.bitcoin.it/wiki/Base58Check_encoding
    @staticmethod
    def create(hash160, address_type):
        step1 = address_type.value + hash160
        step2 = double_sha256(step1)
        step3 = step2[0:4]
        step4 = step1 + step3
        return base58_encode(step4)

    def to_wif(self, network, compressed=True):
        return to_wif(self.hash160, network, compressed)

    def __str__(self):
        return self.value
