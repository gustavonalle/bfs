from lib.elliptic import *
import unittest


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
        c = Curve
        n = 0x9305A46DE7FF8EB107194DEBD3FD48AA20D5E7656CBE0EA69D2A8D4E7C67314A
        q = 0x4000000000000000000020108A2E0CC0D99F8A5EF

        res = c.bits2int(n.to_bytes(32, 'big'), q.bit_length())
        self.assertEqual(0x4982D236F3FFC758838CA6F5E9FEA455106AF3B2B, res)

    def test_int2octets(self):
        c = Curve
        x = 0x09A4D6792295A7F730FC3F2B49CBC0F62E862272F
        q = 0x4000000000000000000020108A2E0CC0D99F8A5EF

        res = c.int2octets(x, q.bit_length())
        self.assertEqual(0x009A4D6792295A7F730FC3F2B49CBC0F62E862272F, int.from_bytes(res, 'big'))

    @unittest.skip("WIP")
    def test_sign(self):
        # Test Vectors for RFC 6979 ECDSA, secp256k1, SHA-256
        # (private key, message, expected k, expected signature)
        test_vectors = [
            (0x1, "Satoshi Nakamoto", 0x8F8A276C19F4149656B280621E358CCE24F5F52542772691EE69063B74F15D15,
             "934b1ea10a4b3c1757e2b0c017d0b6143ce3c9a7e6a4a49860d7a6ab210ee3d82442ce9d2b916064108014783e923ec36b49743e2ffa1c4496f01a512aafd9e5"),
            (0x1, "All those moments will be lost in time, like tears in rain. Time to die...",
             0x38AA22D72376B4DBC472E06C3BA403EE0A394DA63FC58D88686C611ABA98D6B3,
             "8600dbd41e348fe5c9465ab92d23e3db8b98b873beecd930736488696438cb6b547fe64427496db33bf66019dacbf0039c04199abb0122918601db38a72cfc21"),
            (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140, "Satoshi Nakamoto",
             0x33A19B60E25FB6F4435AF53A3D42D493644827367E6453928554F43E49AA6F90,
             "fd567d121db66e382991534ada77a6bd3106f0a1098c231e47993447cd6af2d06b39cd0eb1bc8603e159ef5c20a5c8ad685a45b06ce9bebed3f153d10d93bed5"),
            (0xf8b8af8ce3c7cca5e300d33939540c10d45ce001b8f252bfbc57ba0342904181, "Alan Turing",
             0x525A82B70E67874398067543FD84C83D30C175FDC45FDEEE082FE13B1D7CFDF1,
             "7063ae83e7f62bbb171798131b4a0564b956930092b33b07b395615d9ec7e15c58dfcc1e00a35e1572f366ffe34ba0fc47db1e7189759b9fb233c5b05ab388ea"),
            (0xe91671c46231f833a6406ccbea0e3e392c76c167bac1cb013f6f1013980455c2,
             "There is a computer disease that anybody who works with computers knows about. It's a very serious disease and it interferes completely with the work. The trouble with computers is that you 'play' with them!",
             0x1F4B84C23A86A221D233F2521BE018D9318639D5B8BBD6374A8A59232D16AD3D,
             "b552edd27580141f3b2a5463048cb7cd3e047b97c9f98076c32dbdf85a68718b279fa72dd19bfae05577e06c7c0c1900c371fcd5893f7e1d56a37d30174671f6")
        ]

        c = Curve()

        signature = c.sign(test_vectors[0][1].encode(), test_vectors[0][0], SigHash.ALL)
        self.assertEqual(test_vectors[0][3], signature.hex())


if __name__ == '__main__':
    unittest.main()
