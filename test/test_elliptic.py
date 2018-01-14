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


if __name__ == '__main__':
    unittest.main()
