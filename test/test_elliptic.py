import unittest

from lib.elliptic import *


class TestCurve(unittest.TestCase):

    def test_hasPoint(self):
        c = Curve()
        p1 = Point(55066263022277343669578718895168534326250603453777594175500187360389116729240,
                   32670510020758816978083085130507043184471273380659243275938904335757337482424)
        p2 = Point(0xF028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A,
                   0x07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB)
        p3 = Point(1234, 12345)

        self.assertTrue(c.has_point(p1))
        self.assertTrue(c.has_point(p2))
        self.assertFalse(c.has_point(p3))
        self.assertTrue(c.has_point(c.G))

    def test_sum(self):
        c = Curve()
        infinity = Point(None, None)
        self.assertEqual(c.G, c.sum(c.G, infinity))
        self.assertEqual(c.G, c.sum(infinity, c.G))

    def test_bits2int(self):
        n = 0x9305A46DE7FF8EB107194DEBD3FD48AA20D5E7656CBE0EA69D2A8D4E7C67314A
        q = 0x4000000000000000000020108A2E0CC0D99F8A5EF
        c = Curve(q)

        res = c.bits2int(n.to_bytes(32, 'big'))
        self.assertEqual("0x4982d236f3ffc758838ca6f5e9fea455106af3b2b", hex(res))

    def test_int2octets(self):
        x = 0x09A4D6792295A7F730FC3F2B49CBC0F62E862272F
        q = 0x4000000000000000000020108A2E0CC0D99F8A5EF
        c = Curve(q)

        res = c.int2octets(x)
        self.assertEqual("009a4d6792295a7f730fc3f2b49cbc0f62e862272f", res.hex())

    def test_bits2octets(self):
        x = 0xAF2BDBE1AA9B6EC1E2ADE1D694F41FC71A831D0268E9891562113D8A62ADD1BF.to_bytes(32, 'big')
        q = 0x4000000000000000000020108A2E0CC0D99F8A5EF
        c = Curve(q)

        res = c.bits2octets(x)
        self.assertEqual("01795edf0d54db760f156d0dac04c0322b3a204224", res.hex())

    def test_generate_r(self):
        x = 0x09A4D6792295A7F730FC3F2B49CBC0F62E862272F
        q = 0x4000000000000000000020108A2E0CC0D99F8A5EF
        c = Curve(q)
        msg = "sample".encode()

        res = c.generate_r(x, msg)

        self.assertEqual("0x23af4074c90a02b3fe61d286d5c87f425e6bdd81b", hex(res))

    def test_ecdsa(self):
        # Test Vectors for RFC 6979 ECDSA, secp256k1, SHA-256
        # (private key, message, expected k, expected signature)
        test_vectors = [
            (0x1, "Satoshi Nakamoto",
             0x8F8A276C19F4149656B280621E358CCE24F5F52542772691EE69063B74F15D15,
             "934b1ea10a4b3c1757e2b0c017d0b6143ce3c9a7e6a4a49860d7a6ab210ee3d8"
             "2442ce9d2b916064108014783e923ec36b49743e2ffa1c4496f01a512aafd9e5"),

            (0x1, "All those moments will be lost in time, like tears in rain. Time to die...",
             0x38AA22D72376B4DBC472E06C3BA403EE0A394DA63FC58D88686C611ABA98D6B3,
             "8600dbd41e348fe5c9465ab92d23e3db8b98b873beecd930736488696438cb6b"
             "547fe64427496db33bf66019dacbf0039c04199abb0122918601db38a72cfc21"),

            (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140, "Satoshi Nakamoto",
             0x33A19B60E25FB6F4435AF53A3D42D493644827367E6453928554F43E49AA6F90,
             "fd567d121db66e382991534ada77a6bd3106f0a1098c231e47993447cd6af2d06"
             "b39cd0eb1bc8603e159ef5c20a5c8ad685a45b06ce9bebed3f153d10d93bed5"),

            (0xf8b8af8ce3c7cca5e300d33939540c10d45ce001b8f252bfbc57ba0342904181, "Alan Turing",
             0x525A82B70E67874398067543FD84C83D30C175FDC45FDEEE082FE13B1D7CFDF1,
             "7063ae83e7f62bbb171798131b4a0564b956930092b33b07b395615d9ec7e15c5"
             "8dfcc1e00a35e1572f366ffe34ba0fc47db1e7189759b9fb233c5b05ab388ea"),

            (0xe91671c46231f833a6406ccbea0e3e392c76c167bac1cb013f6f1013980455c2,
             "There is a computer disease that anybody who works with computers knows about. It's a "
             "very serious disease and it interferes completely with the work. The trouble with computers "
             "is that you 'play' with them!",
             0x1F4B84C23A86A221D233F2521BE018D9318639D5B8BBD6374A8A59232D16AD3D,
             "b552edd27580141f3b2a5463048cb7cd3e047b97c9f98076c32dbdf85a68718b27"
             "9fa72dd19bfae05577e06c7c0c1900c371fcd5893f7e1d56a37d30174671f6")
        ]

        c = Curve()

        for item in test_vectors:
            private_key = item[0]
            message = item[1].encode()
            expected_k = item[2]
            expected_signature = item[3]

            rfc6979_key = c.generate_r(private_key, message)
            ecdsa = c.ecdsa(private_key, message)

            self.assertEqual(expected_k, rfc6979_key)
            self.assertEqual(expected_signature, format(ecdsa[0], 'x') + format(ecdsa[1], 'x'))

    def test_sign(self):
        payload = int('0x0100000001eccf7e3034189b851985d871f91384b8ee357cd47c3024736e5676eb2debb3f20'
                      '10000001976a914010966776006953d5567439e5e39f86a0d273bee88acffffffff01605af405'
                      '000000001976a914097072524438d003d23a2f23edb65aae1bb3e46988ac0000000001000000', 0)




if __name__ == '__main__':
    unittest.main()
