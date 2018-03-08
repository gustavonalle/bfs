from unittest import TestCase

from lib.B2XSpender import B2XSpender
from lib.keys import PrivateKey
from lib.spender import Utxo, Destination


class TestB2XSpender(TestCase):

    def test_send_to_bech32(self):
        # Generated with regtest
        pk = PrivateKey.from_wif("cVC6z7gnezHZut5yyuCX3x79tfcbauCWiFcBY92Vg4crfu4Maa5B")

        utxo = Utxo("658d10f95cfcee9674e13cdb29007d407ea8c7d2ec6ae5502a3a9aae74890b27", 0,
                    "miVjzzA21B96xva2aCcaUb8h4RFbf6qKBZ", 25, pk)

        spender = B2XSpender()
        spender.add_utxos(utxo)
        # cSYZYCLT1t9WnAQwTNzfPdg3RXySxu1ewVmRZPXsGkdgUnM2T3uL
        spender.add_destinations(Destination(24.9, "tb1qv3ya29z8nddpxkq4dzllzl0ceujacqvw3hjhh9"))

        tx_hex = spender.create_tx().hex()

        expected = ("0200000001270b8974ae9a3a2a50e56aecd2c7a87e407d0029db3ce17496eefc5cf9108d65000000006b48304502"
                    "2100863d673a5932ff107ece66d97c813701f85c228da0ccf6937caaf18b7c765b7802207c7ee2917c5d65874907"
                    "fa14fefcf6f97de4af1f79fdea4c9182afc860fb519d3121030f96812693c4a50162134cfa307afb63580171963d"
                    "6c4198e8e5cfeee2c92b60ffffffff0180626a94000000001600146449d514479b5a13581568bff17df8cf25dc01"
                    "8e00000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2wpkh(self):
        # Generated with regtest with cmd line ./bitcoin2x-qt -regtest -prematurewitness
        pk = PrivateKey.from_wif("cSYZYCLT1t9WnAQwTNzfPdg3RXySxu1ewVmRZPXsGkdgUnM2T3uL")

        utxo = Utxo("207d7cfb444c26a22bb7fb9eee72ff9bc0abc09d571254b3192024320215954c", 0,
                    "tb1qv3ya29z8nddpxkq4dzllzl0ceujacqvw3hjhh9", 24.9, pk)

        spender = B2XSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(24.8, "mxoVHNnvAEGYCFdPRR8yJw1yuuZfzkr2e7"))

        tx_hex = spender.create_tx().hex()

        expected = ("020000000001014c95150232242019b35412579dc0abc09bff72ee9efbb72ba2264c44fb7c7d200000000000fffff"
                    "fff0100ccd193000000001976a914bd9aa9556109944bb1d984286eec13199c723deb88ac02473044022026892552"
                    "385d049b847e15c8436fc1053fc4c50f376f9dcf7520cbfc2d6ed8cf022078d323b34aa09845c8d362007c2bf7204"
                    "463cc4911b27f0e1814aa51181f5db4312102aa81267011ee208bef8843ceb883e45f4ab13f5dc2f4e17b7781d624"
                    "5bab292600000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2pkh(self):
        # Generated with regtest
        pk = PrivateKey.from_wif("cVC6z7gnezHZut5yyuCX3x79tfcbauCWiFcBY92Vg4crfu4Maa5B")

        utxo = Utxo("b6d073333c1a8e4360b1e2c7fa2ed6b67b74272ad7fabf52a4e4732df5f47dbd", 0,
                    "miVjzzA21B96xva2aCcaUb8h4RFbf6qKBZ", 50, pk)

        spender = B2XSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(49.960, "mrVqpGm7F5MVCwsP4s3fQEN2GAaykJoTu4"))

        tx_hex = spender.create_tx().hex()

        expected = ("0200000001bd7df4f52d73e4a452bffad72a27747bb6d62efac7e2b160438e1a3c3373d0b6000000006a473044022"
                    "01df7c8c97443bd46da751e0051a4395ba3613be3604be97d3c801c21e3d23c79022012ad30b7ffd42ad7bb96f915"
                    "7519f7e3c35409ed54f783a3c854a596343a6c713121030f96812693c4a50162134cfa307afb63580171963d6c419"
                    "8e8e5cfeee2c92b60ffffffff0100e9c829010000001976a91478738f2c5a75397eb2f851597261f766a67d9b6388"
                    "ac00000000")

        self.assertEqual(expected, tx_hex)
