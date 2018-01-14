from lib.transaction import *
import unittest


class TestTransaction(unittest.TestCase):

    def test_varint(self):
        varint = Encoder.to_varint

        self.assertEqual(varint(0).hex(), '00')
        self.assertEqual(varint(4).hex(), '04')
        self.assertEqual(varint(15).hex(), '0f')
        self.assertEqual(varint(106).hex(), '6a')
        self.assertEqual(varint(139).hex(), '8b')
        self.assertEqual(varint(550).hex(), 'fd2602')
        self.assertEqual(varint(998000).hex(), 'fe703a0f00')

    def test_tx_output_p2pkh(self):
        prev_tx = 0xab68025513c3dbd2f7b92a94e0581f5d50f654e7
        vout = TransactionOutput(1500000, prev_tx, SpendType.P2PKH)

        expect = 0x60e31600000000001976a914ab68025513c3dbd2f7b92a94e0581f5d50f654e788ac
        self.assertEqual(expect, int.from_bytes(vout.serialize(), 'big'))


if __name__ == '__main__':
    unittest.main()
