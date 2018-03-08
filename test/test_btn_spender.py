from unittest import TestCase

from lib.BTNSpender import BTNSpender
from lib.keys import PrivateKey
from lib.spender import Utxo, Destination


class TestBTNSpender(TestCase):

    def test_send_to_bech32(self):
        pk = PrivateKey.from_wif("cR735DHmZMw1KGAoLaKeCNYTY1iBQ2hwYs73xGTSMGrpXKG8y2bV")

        utxo = Utxo("2ab1ad93934c2c02060a42cf71e9a37556929679dc78e9d18ec0d01951e2bc62", 0,
                    "mptcoGaQcovBDqJEXyf8XRUdTGYPCfFxq1", 7.99, pk)

        spender = BTNSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(7.98, "tb1quhs3fvy00aq80zcgvtdd9rrt835ecch4ay5ys2"))

        tx_hex = spender.create_tx().hex()

        expected = ("020000000162bce25119d0c08ed1e978dc7996925675a3e971cf420a06022c4c9393adb12a"
                    "000000006a47304402206a71dcec6f1f8850e930372de047164b2a4a4bb6e6ec47af134ae5"
                    "0b0997537902202f22db1c2b77a9458bdd2783c9c691bf654c0066acb3c5832000c7bb2f86"
                    "7a6a412103885eee783dfc7892f354544796be139324f637c8da33655b53852fcbf3d6d65d"
                    "ffffffff018083902f00000000160014e5e114b08f7f40778b0862dad28c6b3c699c62f500"
                    "000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2wpkh(self):
        pk = PrivateKey.from_wif("cS8ycBgjYBuNgeBacXRbvbAtbqoki13yUond8NKnipyFzyMrJc6m")

        utxo = Utxo("f46bd6e93fdd51876c2d7639cfd705b82c60b8301f2a8479b80585ed9b246826", 0,
                    "tb1quhs3fvy00aq80zcgvtdd9rrt835ecch4ay5ys2", 7.98, pk)

        spender = BTNSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(7.97, "mqmXo6XKQYgPHVS4zFS6MApdpXcMs47vda"))

        tx_hex = spender.create_tx().hex()

        expected = ("020000000001012668249bed8505b879842a1f30b8602cb805d7cf39762d6c8751dd3fe9d66bf"
                    "40000000000ffffffff014041812f000000001976a91470730bda4463441b52a393ccced5aab0"
                    "77cb4cae88ac02483045022100f3e47f61407c6d7f620c78ba56a65a285f7483e85f06da35014"
                    "101808d75931c0220638a8a91fa8b1d747da9dc04730ed161c12e44f4e7e39ff9066e00277492"
                    "468d41210358848ad624557628636d72e290c259478774504072b8504a6bb7ea7bb51c8d32000"
                    "00000")

        self.assertEqual(expected, tx_hex)

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
