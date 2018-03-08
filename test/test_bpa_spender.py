from unittest import TestCase

from lib.BPASpender import BPASpender
from lib.keys import PrivateKey
from lib.spender import Utxo, Destination


class TestBPASpender(TestCase):

    def test_spend_p2wpkh(self):
        pk = PrivateKey.from_wif("L1yDt2VzCMQHoHwbtwwXgvgR3eTSTrnX681rZo1ZP77mWYBXLz1R")

        utxo = Utxo("6be023686146f09cd04a2c00183fad462dd6695cf174e4d42ab9024a57055351", 0,
                    "tb1qra8njpfw75hcu4s6ad687xrtemddzjrz5pfjsy", 9.95000001, pk)

        spender = BPASpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(9.94, "mpLNpwccBEZxv729ds8ne2eE7h1Twqmq6q"))

        tx_hex = spender.create_tx().hex()

        expected = ("02000000000101515305574a02b92ad4e474f15c69d62d46ad3f18002c4ad09cf046616823e06b000000"
                    "0000ffffffff01803c3f3b000000001976a91460b909046298988c59767c0343dd424ebf79ba6c88ac02"
                    "483045022100dced32a6e20d2bdab81e9ac6e0912b92c1633f70368eb5c04408049d8668188e0220468b"
                    "df80a6f3706758820f9d825735c2222496d0e584d52ac8ce2f761630408e2121023130497ba9dda8f3f2"
                    "9ee662500e1ff5b5d135169a57210c055bff78e75d347300000000")

        self.assertEqual(expected, tx_hex)

    def test_send_to_bech32(self):
        pk = PrivateKey.from_wif("cQzqkdWwGaRfY7KK5jLt6uEvTxWDZXXhRUcdY9Eaz6Geq81685BX")

        utxo = Utxo("243e1aa0b5cb8134a91f63a09523831bd1245683549a574f1b5c997fb89d1ebf", 0,
                    "n2njoVpqeoCupZhqt8myDnWaLFzirbgHtQ", 9.96000001, pk)

        spender = BPASpender()
        spender.add_utxos(utxo)

        spender.add_destinations(Destination(9.95000001, "tb1qra8njpfw75hcu4s6ad687xrtemddzjrz5pfjsy"))

        tx_hex = spender.create_tx().hex()

        expected = ("0200000001bf1e9db87f995c1b4f579a54835624d11b832395a0631fa93481cbb5a01a3e24000000006"
                    "a47304402201ca4637fdd04626457ec528878b902220e29af6ca6696ce36b5d904f9dcbe1ec02205466"
                    "224c1817f09244de7aaf7a12b3c5f0e8736ce840fc415e89196cacd92b4421210331a2c9442b1c0cbd0"
                    "c1d5a291bc863cf11ebbc26537f1602d1d0a6a30d5725cbffffffff01c17e4e3b000000001600141f4f"
                    "39052ef52f8e561aeb747f186bcedad1486200000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2pkh(self):
        pk = PrivateKey.from_wif("cQzxzNwiXTds7Aa26xX2po8H6iVMo4R7ZbvW3sohkchNnkXir3cz")

        utxo = Utxo("a550c89a0a8711dad2998614be0d05d237cb6deaf92edbbbc62884d479cd9721", 0,
                    "mzTfa7VEwjpuYYDkqxEFDwurDifruWWVaN", 9.98, pk)

        spender = BPASpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(9.96, "n2njoVpqeoCupZhqt8myDnWaLFzirbgHtQ"))

        tx_hex = spender.create_tx().hex()

        expected = ("02000000012197cd79d48428c6bbdb2ef9ea6dcb37d2050dbe148699d2da11870a9ac850a500000000"
                    "6b483045022100d75d05c1813d5b4ff0951b05b54a1419a80583a4f21731d0ed2989ef7c8235ce0220"
                    "5676dca70070f7982a3fc4dc1ecffd924efb59be7971781c227faaa1090e732b212102f2d6f4327cd0"
                    "870c1fd15effc3bf56acdc5a0d0e5b9c0fb11815e8e5b613b822ffffffff0101c15d3b000000001976"
                    "a914e956de67151c4c604861aa3d3ea05a2628a0ac0888ac00000000")

        self.assertEqual(expected, tx_hex)
