import unittest

from lib.transaction import *
from lib.utils import *


class TestTransaction(unittest.TestCase):

    def test_varint(self):
        self.assertEqual(to_varint(0).hex(), '00')
        self.assertEqual(to_varint(4).hex(), '04')
        self.assertEqual(to_varint(15).hex(), '0f')
        self.assertEqual(to_varint(106).hex(), '6a')
        self.assertEqual(to_varint(139).hex(), '8b')
        self.assertEqual(to_varint(550).hex(), 'fd2602')
        self.assertEqual(to_varint(998000).hex(), 'fe703a0f00')

    def test_tx_output_p2pkh(self):
        prev_tx = 0xab68025513c3dbd2f7b92a94e0581f5d50f654e7
        vout = TransactionOutput(1500000, prev_tx, SpendType.P2PKH)

        expect = 0x60e31600000000001976a914ab68025513c3dbd2f7b92a94e0581f5d50f654e788ac
        self.assertEqual(expect, self.to_int(vout.serialize()))

    def test_tx_output_p2wpkh(self):
        prev_tx = 0xab68025513c3dbd2f7b92a94e0581f5d50f654e7
        vout = TransactionOutput(1500000, prev_tx, SpendType.P2WPKH)

        expect = 0x60e3160000000000160014ab68025513c3dbd2f7b92a94e0581f5d50f654e7
        self.assertEqual(expect, self.to_int(vout.serialize()))

    def test_P2PKH_RawTx_SingleInput_SingleOutput(self):
        # Inputs
        prev_tx = "d53b66eea5c5ff7d8a2ab9b03187acca52538c861298f550727e87176a38241d"
        prev_script = "76a914f13bdea27f1fdfb164d083dd827ff55eb140d68688ac"
        prev_idx = 0

        # Outputs
        hash160_output = 0xa1f856634fdac51ede71a2a13585735568470785
        amount = 71943072

        expected = ("01000000011d24386a17877e7250f59812868c5352caac8731b0b92a8a7dffc5a"
                    "5ee663bd5000000001976a914f13bdea27f1fdfb164d083dd827ff55eb140d686"
                    "88acffffffff01a0c34904000000001976a914a1f856634fdac51ede71a2a1358"
                    "573556847078588ac00000000")

        tx_in = TransactionInput(prev_tx, prev_idx, prev_script, SpendType.P2PKH)
        tx_out = TransactionOutput(amount, hash160_output, SpendType.P2PKH)

        tx = Transaction()
        tx.add_inputs(tx_in)
        tx.add_outputs(tx_out)

        raw = tx.serialize()

        self.assertEqual(expected, raw.hex())

    def test_P2PKH_RawTx_SingleInput_SingleOutput_2(self):
        # Inputs
        prev_tx = "e220edf4ac210e74443cd28661d185d42664977151c277ed07a058ba07df24d4"
        prev_script = "76a9143f16f9b73c09a678997c6e479efae2c0df6feb9e88ac"
        prev_idx = 8

        # Outputs
        hash160_output = 0xa1f856634fdac51ede71a2a13585735568470785
        amount = 591117

        expected = ("0100000001d424df07ba58a007ed77c25171976426d485d16186d23c44740e21"
                    "acf4ed20e2080000001976a9143f16f9b73c09a678997c6e479efae2c0df6feb"
                    "9e88acffffffff010d050900000000001976a914a1f856634fdac51ede71a2a1"
                    "358573556847078588ac00000000")

        tx_in = TransactionInput(prev_tx, prev_idx, prev_script, SpendType.P2PKH)
        tx_out = TransactionOutput(amount, hash160_output, SpendType.P2PKH)

        tx = Transaction()
        tx.add_inputs(tx_in)
        tx.add_outputs(tx_out)

        raw = tx.serialize()

        self.assertEqual(expected, raw.hex())

    def test_P2PKH_RawTx_MultipleInput_SingleOutput(self):
        # Inputs
        prev_tx_1 = "8ab885867092db0d1a7220fc8bb0b549c156ea7bb69435a08161bdcbd8864f46"
        prev_idx_1 = 2
        prev_script_1 = "76a914e58b5ca8dedf22a4e86ebfa3a6ac0a595abf887688ac"
        value_1 = 91520573

        prev_tx_2 = "8d097c739096828989427f1a00910996fd14c6c2d322fd559e9b68ef43d25024"
        prev_idx_2 = 0
        prev_script_2 = "76a9146ae01d93e035b5724748b427d9d565c18a44885a88ac"
        value_2 = 416110

        # Outputs
        address = "16Fg2yjwrbtC6fZp61EV9mNVKmwCzGasw5"
        hash160 = int.from_bytes(hash160_from_address(address), 'big')
        amount = (value_1 + value_2) - 1

        expected = ("0100000002464f86d8cbbd6181a03594b67bea56c149b5b08bfc20721a0ddb927086"
                    "85b88a020000001976a914e58b5ca8dedf22a4e86ebfa3a6ac0a595abf887688acff"
                    "ffffff2450d243ef689b9e55fd22d3c2c614fd960991001a7f428989829690737c09"
                    "8d000000001976a9146ae01d93e035b5724748b427d9d565c18a44885a88acffffff"
                    "ff01aad77a05000000001976a914399f09529a1e7f37ff5a892644b47690ab5e516f"
                    "88ac00000000")

        tx_in_1 = TransactionInput(prev_tx_1, prev_idx_1, prev_script_1, SpendType.P2PKH)
        tx_in_2 = TransactionInput(prev_tx_2, prev_idx_2, prev_script_2, SpendType.P2PKH)
        tx_out = TransactionOutput(amount, hash160, SpendType.P2PKH)

        tx = Transaction()
        tx.add_inputs(tx_in_1, tx_in_2)
        tx.add_outputs(tx_out)

        raw = tx.serialize()

        self.assertEqual(expected, raw.hex())

    @staticmethod
    def to_int(b):
        return int.from_bytes(b, 'big')


if __name__ == '__main__':
    unittest.main()
