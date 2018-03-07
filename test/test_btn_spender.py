from unittest import TestCase

from lib.BTNSpender import BTNSpender
from lib.keys import PrivateKey
from lib.spender import Utxo, Destination


class TestBTNSpender(TestCase):

    def test_spend_p2pkh(self):
        pk = PrivateKey.from_wif("cU4TK4AU8zCSVAwPkBdgreQauTnMSERoiFpvd1MJtyavD27fpYL2")

        utxo = Utxo("dc719183637718c2958bfa565d93416824a4ee55e5524521dbad672bfbd88947", 1,
                    "mgWwTDdpMawWS7aeTmZ3qmDwECvHtbZyBf", 8, pk)

        spender = BTNSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(7.99, "mptcoGaQcovBDqJEXyf8XRUdTGYPCfFxq1"))

        tx_hex = spender.create_tx().hex()

        expected = ("02000000014789d8fb2b67addb214552e555eea4246841935d56fa8b95c2187763839171dc01000000"
                    "6a47304402206b4a9264a2617d9aa1c280832240ae2180e6e5ab83afefc3a9116ca9ebcd9006022078"
                    "c72fe4ed38f562014a088280fb218cef43203689c84a0bf7dd0c708855575f412103db27f9d7a206f7"
                    "7fd904c779709b1589844c1d3afb2b2a223eb106ca9481430cffffffff01c0c59f2f000000001976a9"
                    "1466d2022f2ef98cc32f8c58d198b9fe1b82a6665588ac00000000")
        self.assertEqual(expected, tx_hex)
