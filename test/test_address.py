import unittest

from lib.address import *
from lib.commons import hash160_from_address
from lib.transaction import SpendType


class TestAddress(unittest.TestCase):

    def test_base58_encode(self):
        # hash160, address, net
        vector = [
            (0x60df6799ffa4a1060b40460ecc98c4ca7104576b, "19qDVr4oLSAEXeJ3xzvtwHzBd4KpCQuv1o", Network.MAIN_NET),
            (0x66a9b31e2b9d5101a11a72a22c600f80cb002f47, "1AMqDWQwYimRmYdC4jsWuhLzhQzCYcc2of", Network.MAIN_NET),
            (0x71645c16939c68c6446b6bfdd22c39ac7050fd1b, "mqrWsr3bWegBEtdb7obPFr4CxfSHofy7dQ", Network.TEST_NET),
            (0x01137267db64b01433d91c5e70ee193ed590df04, "mfceGSUGyMYj4ezk75vPJmKBB74uTzAaeJ", Network.TEST_NET)
        ]

        for item in vector:
            hash160_bytes = item[0].to_bytes(20, 'big')
            address_str = item[1]
            net = item[2]

            address = AddressV1(hash160_bytes, net)
            self.assertEqual(address_str, address.value)
            self.assertEqual(hash160_bytes, hash160_from_address(address.value, SpendType.P2PKH))

    def test_bech32(self):
        vector = [
            ("tb1qrlx6pqm5lrzg2jus7kxx3u7cypftcruqk42lcf",
             0x1fcda08374f8c4854b90f58c68f3d82052bc0f80,
             Network.TEST_NET),
            ("bc1ql2yexu5unurt8ullfjt6nx4fnz8gtfgcuydejn",
             0xfa8993729c9f06b3f3ff4c97a99aa9988e85a518,
             Network.MAIN_NET),
            ("bc1qc235rpvagps8p7249tq554lnfctm27sjlzzrut",
             0xc2a341859d406070f9552ac14a57f34e17b57a12,
             Network.MAIN_NET)
        ]

        for item in vector:
            address = item[0]
            hash160 = item[1].to_bytes(20, 'big')
            net = item[2]

            # Hash160 -> Bech32
            result = Bech32Address.from_hash160(hash160, net)
            self.assertEqual(address, result.value)

            # bech32 -> Hash160
            decoded_hash_160 = Bech32Address.from_address(address).hash160
            self.assertEqual(decoded_hash_160, hash160)

    def test_satoshi_btc(self):
        btc = 123456677.00000001
        self.assertEqual(btc, satoshis_to_btc(btc_to_satoshis(btc)))

        btc = 9.96
        self.assertEqual(btc, satoshis_to_btc(btc_to_satoshis(btc)))
