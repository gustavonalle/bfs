from unittest import TestCase

from lib.bci import BCISpender
from lib.keys import PrivateKey
from lib.spender import Utxo, Destination


class TestBCISpender(TestCase):

    def test_send_to_bech32(self):
        pk = PrivateKey.from_wif("cTBQFX1uQDsc8EynnUbjqGp141Meh8bL25QCFxJDYRawkoShcs5S")

        utxo = Utxo("5e802945886221fa9ab51ae00d8c412f5237220dfe60470de5580200453c1895", 0,
                    "ms8T2Mki2Cy4AkYZynnVVoXKnt4R87pXK3", 10, pk)

        spender = BCISpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(9.993, "tb1qvnwx4vgelj3dlnp7s7uahaa45ck3esvh32eh80"))

        tx_hex = spender.create_tx().hex()

        expected = ("020000000195183c45000258e50d4760fe0d2237522f418c0de01ab59afa2162884529805e0000"
                    "00006b4830450221008b84ad2ef7d59cf7c0b49aad0a18b8da8e715f4609e1cd89f285daa6715b"
                    "e3a7022057f2592aa709f8ee2d366aeb191b19993be36086e2807eafb3aff3d1764bcc8c412103"
                    "4a41adc833d2c2c05596863e1eafb0d631ab47d03ebdc0d534de70bb8aa4301effffffff01a01b"
                    "903b0000000016001464dc6ab119fca2dfcc3e87b9dbf7b5a62d1cc19700000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2wpkh(self):
        pk = PrivateKey.from_wif("KzGv8HkggHyio1vGGF1Z7sQERvknpMKg82qr4uhmkJn4PBDefyRv")

        utxo = Utxo("a53044b74dd42a45aae1f693949423f33c9f0be0941475cceb02579bdd76ca92", 0,
                    "tb1qvnwx4vgelj3dlnp7s7uahaa45ck3esvh32eh80", 9.993, pk)

        spender = BCISpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(9.98, "ms8T2Mki2Cy4AkYZynnVVoXKnt4R87pXK3"))

        tx_hex = spender.create_tx().hex()

        expected = ("0200000000010192ca76dd9b5702ebcc751494e00b9f3cf323949493f6e1aa452ad44db74430a5000"
                    "0000000ffffffff0180457c3b000000001976a9147f5feca396a2e8cbf290753af7d47a6493ff46b4"
                    "88ac0247304402204c195e4e9bcac037db01cc65231d750a8f887185152f2dbb1ef750c786fdf75f0"
                    "22043a4abf181e3f6a6a01fc7ff3799a74adeedbfb0967a90e8fa9c90581f36ce3e412102e959fb1b"
                    "bb68cb44ed91739befc1dd93f47998b8d74eb34ff0e71da4c921e42a00000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2pkh(self):
        pk = PrivateKey.from_wif("cRE4ietJxmEyum3SHny9quVLTY9k7XZ9tKvqyctVMHaYA7zhfrJE")

        utxo = Utxo("eeae2d76ed671015f47f8103533aeed4ef0b0557156657b5b2774a44c7780abe", 0,
                    "mzw8EynNdyR2jzE8cXktpiTU7oGs1MURdA", 10, pk)

        spender = BCISpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(9.9999, "mh77F22aAnE4uF6CourTRpRCRLCUPTUVo2"))

        tx_hex = spender.create_tx().hex()

        expected = ("0200000001be0a78c7444a77b2b557661557050befd4ee3a5303817ff4151067ed762"
                    "daeee000000006b483045022100faef70293f42675ef9ca6df584c3e83a156ea30346"
                    "59ea8abeb033e589cbe69a02204fc86dabbac7ddbe5d6f10d6199d1133bab07d1cfad"
                    "33ccb69aa1bbcc21020fd412102f2fcf143b17f6763a4e633a6565f4d56711e1eede6"
                    "41473027db2eb07227f241ffffffff01f0a29a3b000000001976a914116dbcd48cf8b"
                    "3d0498852b1e4bc0a6ab17d9b4688ac00000000")

        self.assertEqual(expected, tx_hex)
