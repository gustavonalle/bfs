import unittest

from lib.address import *
from lib.utils import hash160_from_address


class TestAddress(unittest.TestCase):

    def test_base58_encode(self):
        # hash160, address, net
        vector = [
            (0x60df6799ffa4a1060b40460ecc98c4ca7104576b, "19qDVr4oLSAEXeJ3xzvtwHzBd4KpCQuv1o", AddressType.MAIN_NET),
            (0x66a9b31e2b9d5101a11a72a22c600f80cb002f47, "1AMqDWQwYimRmYdC4jsWuhLzhQzCYcc2of", AddressType.MAIN_NET),
            (0x71645c16939c68c6446b6bfdd22c39ac7050fd1b, "mqrWsr3bWegBEtdb7obPFr4CxfSHofy7dQ", AddressType.TEST_NET),
            (0x01137267db64b01433d91c5e70ee193ed590df04, "mfceGSUGyMYj4ezk75vPJmKBB74uTzAaeJ", AddressType.TEST_NET)
        ]

        for item in vector:
            hash160_bytes = item[0].to_bytes(20, 'big')
            address_str = item[1]
            net = item[2]

            res = create_address_v1(hash160_bytes, net)
            self.assertEqual(address_str, res)
            self.assertEqual(hash160_bytes, hash160_from_address(res))


if __name__ == '__main__':
    unittest.main()
