import unittest

from lib.elliptic import *
from lib.keys import PrivateKey


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

    def test_multiply(self):
        infinity = Point(None, None)
        c = Curve()
        self.assertEqual(c.multiply(c.G, c.n), infinity)

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
        msg = hashlib.sha256("sample".encode()).digest()

        res = c.generate_r(PrivateKey(x), msg)

        self.assertEqual("0x23af4074c90a02b3fe61d286d5c87f425e6bdd81b", hex(res.value()))

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
            pk = item[0]
            message = hashlib.sha256(item[1].encode()).digest()
            expected_k = item[2]
            expected_signature = item[3]

            rfc6979_key = c.generate_r(PrivateKey(pk), message)
            ecdsa = c.ecdsa(PrivateKey(pk), message)

            self.assertEqual(expected_k, rfc6979_key.value())
            self.assertEqual(expected_signature, format(ecdsa[0], 'x') + format(ecdsa[1], 'x'))

    def test_DER(self):
        c = Curve()
        # Private Key, Message, Expected DER Signature
        test_vectors = [
            (0x0000000000000000000000000000000000000000000000000000000000000001,
             "Everything should be made as simple as possible, but not simpler.",
             "3044022033a69cd2065432a30f3d1ce4eb0d59b8ab58c74f27c41a7fdb5696ad4e6108"
             "c902206f807982866f785d3f6418d24163ddae117b7db4d5fdf0071de069fa54342262"
             ),
            (0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140,
             "Equations are more important to me, because politics is for the present,"
             " but an equation is something for eternity.",
             "3044022054c4a33c6423d689378f160a7ff8b61330444abb58fb470f96ea16d99d4a2fe"
             "d022007082304410efa6b2943111b6a4e0aaa7b7db55a07e9861d1fb3cb1f421044a5"
             ),
            (0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140,
             "Not only is the Universe stranger than we think, it is stranger than we "
             "can think.",
             "3045022100ff466a9f1b7b273e2f4c3ffe032eb2e814121ed18ef84665d0f515360dab3"
             "dd002206fc95f5132e5ecfdc8e5e6e616cc77151455d46ed48f5589b7db7771a332b283"
             ),
            (0x0000000000000000000000000000000000000000000000000000000000000001,
             "How wonderful that we have met with a paradox. Now we have some hope of "
             "making progress.",
             "3045022100c0dafec8251f1d5010289d210232220b03202cba34ec11fec58b3e93a85b91"
             "d3022075afdc06b7d6322a590955bf264e7aaa155847f614d80078a90292fe205064d3"
             ),
            (0x69ec59eaa1f4f2e36b639716b7c30ca86d9a5375c7b38d8918bd9c0ebc80ba64,
             "Computer science is no more about computers than astronomy is about telescopes.",
             "304402207186363571d65e084e7f02b0b77c3ec44fb1b257dee26274c38c928986fea45d"
             "02200de0b38e06807e46bda1f1e293f4f6323e854c86d58abdd00c46c16441085df6"
             ),
            (0x00000000000000000000000000007246174ab1e92e9149c6e446fe194d072637,
             "...if you aren't, at any given time, scandalized by code you wrote five or even "
             "three years ago, you're not learning anywhere near enough",
             "3045022100fbfe5076a15860ba8ed00e75e9bd22e05d230f02a936b653eb55b61c99dda48"
             "702200e68880ebb0050fe4312b1b1eb0899e1b82da89baa5b895f612619edf34cbd37"
             ),
            (0x000000000000000000000000000000000000000000056916d0f9b31dc9b637f3,
             "The question of whether computers can think is like the question of whether "
             "submarines can swim.",
             "3045022100cde1302d83f8dd835d89aef803c74a119f561fbaef3eb9129e45f30de86abbf90"
             "22006ce643f5049ee1f27890467b77a6a8e11ec4661cc38cd8badf90115fbd03cef"
             ),
            (28,
             "Caught between a rock and a hard place.",
             "3045022100d364c3fc66e4c2df234809f8887fc0fa996c819f7c53a8db3e5a25677b492c9502"
             "201bdcecf0b8c362929626164e734739f74430aab3ea16a62fff87bbc4b08d3ebe"),
            (71066220492785796115493323581994430418788261467619766175488093873426581002692,
             "Beauty is in the eye of the beholder.",
             "30440220306a8ee0c28bf4acfbfea5d63a61762dec700f5d32dd0d8def4fe862b6d3b4760220"
             "30ea9f381465614c5d4ebcebd4a2b57e9f8f913bf1532571f3026bc55282987e")
        ]

        for item in test_vectors:
            pk = item[0]
            message = hashlib.sha256(item[1].encode()).digest()
            expected_der = item[2]

            signature = c.sign(message, PrivateKey(pk))

            self.assertEqual(expected_der, signature.hex(), message)


if __name__ == '__main__':
    unittest.main()
