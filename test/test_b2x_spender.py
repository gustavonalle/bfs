from unittest import TestCase

from lib.B2XSpender import B2XSpender
from lib.keys import PrivateKey
from lib.spender import Utxo, Destination


class TestB2XSpender(TestCase):

    def test_spend_bech32(self):
        pk = PrivateKey.from_wif("LEDZf6CbScCzSxpHHEkb23cstcvrzZMLFws7Px2BBa8atj4vabN9")

        utxo = Utxo("2b34bb178f07d143de91764d4e7d1c2c031975ecf1a7a2a0d4131445a3373b5b", 0,
                    "bc1qvhgz26zt27zu45jqe8tjsgctv20xy7u43n4e9u", 0.00010000, pk)

        spender = B2XSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(0.00001001, "1P7w6ur2WZRceFHTPWMd65P2p8K2mEHEBe"))

        tx_hex = spender.create_tx().hex()

        expected = ("010000000001015b3b37a3451413d4a0a2a7f1ec7519032c1c7d4e4d7691de43d1078f17bb"
                    "342b0000000000ffffffff01ea030000000000001976a914f2a26cce0a92ca350bf204ed8d"
                    "4c94bf2ea2d8d388ac024830450221009fbebefd4435b6ef827b39be01503fc712c4664b22"
                    "447acbadeaaa40c7dff7a7022079e95c9cd4a3bed2ea6a87cac971b8d11f1b5b1f0238c496"
                    "28f09084ad72998e212103cb263a76efe6fce59b02ae64b8d11dd5022a272704c7f3eb44e2"
                    "44197dfb03b000000000")

        self.assertEqual(expected, tx_hex)
