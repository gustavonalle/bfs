from unittest import TestCase

from lib.btv import BTVSpender
from lib.keys import PrivateKey
from lib.spender import Utxo, Destination


class TestBTVSpender(TestCase):

    def test_send_to_bech32(self):
        pk = PrivateKey.from_wif("cUio9ok9CXDfByfGEiRi8snZmwSaAbnvdbmfg72wegPdkX4b7Cq5")

        utxo = Utxo("b7b3b915e7b90f57426e18aeb4f5d42a1189902122a11278c432b0b74cf7cede", 0,
                    "msDmp5xD5hNLsiyasWjNpuxPuz1BfY2G9R", 9.96, pk)

        spender = BTVSpender()
        spender.add_utxos(utxo)
        # cSYZYCLT1t9WnAQwTNzfPdg3RXySxu1ewVmRZPXsGkdgUnM2T3uL
        spender.add_destinations(Destination(9.9, "tb1qv3ya29z8nddpxkq4dzllzl0ceujacqvw3hjhh9"))

        tx_hex = spender.create_tx().hex()

        expected = ("0200000001decef74cb7b032c47812a122219089112ad4f5b4ae186e42570fb9e715b9b3b700000000"
                    "6a47304402204e8d98dc8038641ed72712b939a885d4c70b9d30360311a86bd0273f2ae9b116022030"
                    "d73e717711a7f6d9488557bab272e64d3c4a0618c4e5259ad593d316ad6415412103e9745d6b951c47"
                    "251c63e7677985c2e8f90a85073c9a9461485f7711f3a66707ffffffff018033023b00000000160014"
                    "6449d514479b5a13581568bff17df8cf25dc018e00000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2wpkh(self):
        pk = PrivateKey.from_wif("cSYZYCLT1t9WnAQwTNzfPdg3RXySxu1ewVmRZPXsGkdgUnM2T3uL")

        utxo = Utxo("824799a7d3e9cc4227bc36e0bb6d11d750a87b4483f6454c4804ad2222581b8f", 0,
                    "tb1qv3ya29z8nddpxkq4dzllzl0ceujacqvw3hjhh9", 9.90, pk)

        spender = BTVSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(9.89998999, "msDmp5xD5hNLsiyasWjNpuxPuz1BfY2G9R"))

        tx_hex = spender.create_tx().hex()

        expected = ("020000000001018f1b582222ad04484c45f683447ba850d7116dbbe036bc2742cce9d3a79947820000000"
                    "000ffffffff01972f023b000000001976a9148061b01d9ad56cbe943fe4b55ab4629136a3596e88ac0248"
                    "3045022100b791b0e3119daded4d133ed9f256d524cc6ede34149b6e469a14ab15ce01eba002206d28172"
                    "369cfcf8a5aa04e441df337a73888f019726d55a791033a47e0ae550f412102aa81267011ee208bef8843"
                    "ceb883e45f4ab13f5dc2f4e17b7781d6245bab292600000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2pkh(self):
        pk = PrivateKey.from_wif("cUio9ok9CXDfByfGEiRi8snZmwSaAbnvdbmfg72wegPdkX4b7Cq5")

        utxo = Utxo("c9338d3cb5ce17fcfaee8ccadd7513110aee3148fbce1bc978d245d180fd7ad8", 1,
                    "msDmp5xD5hNLsiyasWjNpuxPuz1BfY2G9R", 10, pk)

        spender = BTVSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(9.960, "msDmp5xD5hNLsiyasWjNpuxPuz1BfY2G9R"))

        tx_hex = spender.create_tx().hex()

        expected = ("0200000001d87afd80d145d278c91bcefb4831ee0a111375ddca8ceefafc17ceb53c8d33c9010000006a4730440220"
                    "1d751f140d560c127ab6f3583dd9052c7556cd9457baa59c4087350840182f9b0220296cdbabb280591ef013a15e97"
                    "5c93e2cedb8c6fa30f9eed359a2bb125847562412103e9745d6b951c47251c63e7677985c2e8f90a85073c9a946148"
                    "5f7711f3a66707ffffffff0100c15d3b000000001976a9148061b01d9ad56cbe943fe4b55ab4629136a3596e88ac00"
                    "000000")

        self.assertEqual(expected, tx_hex)
