from unittest import TestCase

from lib.keys import PrivateKey
from lib.spender import Utxo, Spender, Destination


class TestSpender(TestCase):

    def test_spend_multiple_inputs(self):
        pk = PrivateKey.from_wif("91r82bjCYhYnimoCoqySeNk9AMaHFgPEedzXSCwb39vHiZLSBCQ")

        utxo1 = Utxo("24b0d378e09fb5f726f2c2e5373463276e1c9e9aed4e5907ae139741ec722e2f", 0,
                     "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4", 0.99994220, pk)
        utxo2 = Utxo("beb74ea7c6cc3a8875acaeb23f117d4b9408d8d684355b27e605ab38c1edf854", 0,
                     "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4", 0.21594873, pk)
        utxo3 = Utxo("8df2ad0242b7634fe082c5b2e92c41d550c6cf0b5083f944677a42c69f90bc3d", 0,
                     "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4", 0.09979705, pk)
        utxo4 = Utxo("7a763bc6ea8f790766835459d7f0735c6952bfe9a5ed3220f12f536a7ff59743", 0,
                     "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4", 0.06530584, pk)

        spender = Spender()
        spender.add_utxos(utxo1)
        spender.add_utxos(utxo2)
        spender.add_utxos(utxo3)
        spender.add_utxos(utxo4)
        spender.add_destinations(Destination(1.38, "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4"))

        tx_hex = spender.create_tx().hex()

        expected = ("02000000042f2e72ec419713ae07594eed9a9e1c6e27633437e5c2f226f7b59fe078d3b02400000000"
                    "8b483045022100884d06e7b7515afb20062b2e855a224357a8731aba085eee2910e7416a15ca9f0220"
                    "63969980c89cd112d23d09abed52db857a00dc634e0106b5eec01c4ea67d85f5014104dc406568adad"
                    "d693f302205af9694bf3caf3da0374f2183bea4680fb0d1f5cf5f06c2a78a0229129023260658e4e9f"
                    "37d7d9e22fad81dfdbb944163138a82b68ffffffff54f8edc138ab05e6275b3584d6d808944b7d113f"
                    "b2aeac75883accc6a74eb7be000000008b483045022100daf2b144c38ca30eb74aa62aed2814833260"
                    "e7e4ab1edfe4fa97311b7ba6228402207699e6287073bf41e8f9113efa5b697004d8978c1939b57569"
                    "186d4dfcefb9c4014104dc406568adadd693f302205af9694bf3caf3da0374f2183bea4680fb0d1f5c"
                    "f5f06c2a78a0229129023260658e4e9f37d7d9e22fad81dfdbb944163138a82b68ffffffff3dbc909f"
                    "c6427a6744f983500bcfc650d5412ce9b2c582e04f63b74202adf28d000000008b483045022100d75d"
                    "de09a577a3d481fc2757490ccc8f65fd81a380e039475fb39114b1a34dff0220776d31bcc3f81adb23"
                    "93762494c2424195fcb1ca06bc7595ba352dec69deffbf014104dc406568adadd693f302205af9694b"
                    "f3caf3da0374f2183bea4680fb0d1f5cf5f06c2a78a0229129023260658e4e9f37d7d9e22fad81dfdb"
                    "b944163138a82b68ffffffff4397f57f6a532ff12032eda5e9bf52695c73f0d75954836607798feac6"
                    "3b767a000000008a47304402204d19e36764310b0e70c51f19ff1db582c0b15f7ed36c408119137250"
                    "efec81ee02206851c6247c031407a37c60a920a9f1f03a2bac2ce49a97f76a626fa57c2b6937014104"
                    "dc406568adadd693f302205af9694bf3caf3da0374f2183bea4680fb0d1f5cf5f06c2a78a022912902"
                    "3260658e4e9f37d7d9e22fad81dfdbb944163138a82b68ffffffff0180b63908000000001976a914f1"
                    "3bdea27f1fdfb164d083dd827ff55eb140d68688ac00000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2pkh_to_p2wpkh(self):
        pk = PrivateKey.from_wif("91r82bjCYhYnimoCoqySeNk9AMaHFgPEedzXSCwb39vHiZLSBCQ")

        utxo = Utxo("2df567a8aca645081cb1e56f3a28bdf37c4456b629b00768340afb393446cbf7", 0,
                    "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4", 1.38, pk)

        spender = Spender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(1.37, "tb1qfeytr2u0d3e3tny5kyjvjule3srx33eclcx6sy"))

        tx_hex = spender.create_tx().hex()

        expected = ("0200000001f7cb463439fb0a346807b029b656447cf3bd283a6fe5b11c0845a6aca867f52d00000000"
                    "8a47304402207c6d8871605aea2d02955c04c67a41152ad7efaf28ceba25f74332a0ae252451022000"
                    "e6762e9ce1ee968ed397756bfe18dfb2f185432056e2688bc180f9ec2bcadb014104dc406568adadd6"
                    "93f302205af9694bf3caf3da0374f2183bea4680fb0d1f5cf5f06c2a78a0229129023260658e4e9f37"
                    "d7d9e22fad81dfdbb944163138a82b68ffffffff0140742a08000000001600144e48b1ab8f6c7315cc"
                    "94b124c973f98c0668c73800000000")

        self.assertEqual(expected, tx_hex)
