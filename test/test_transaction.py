import unittest

from lib.keys import PrivateKey, KeyPair, PublicKey
from lib.transaction import *


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
        address = "1GdK9UzpHBzqzX2A9JFP3Di4weBwqgmoQA"
        vout = TransactionOutput(1500000, address, SpendType.P2PKH)

        expect = 0x60e31600000000001976a914ab68025513c3dbd2f7b92a94e0581f5d50f654e788ac
        self.assertEqual(expect, self.to_int(vout.serialize()))

    def test_tx_output_p2wpkh(self):
        address = "tb1qfeytr2u0d3e3tny5kyjvjule3srx33eclcx6sy"
        vout = TransactionOutput(1500000, address, SpendType.P2WPKH)

        expect = 0x60e31600000000001600144e48b1ab8f6c7315cc94b124c973f98c0668c738
        self.assertEqual(expect, self.to_int(vout.serialize()))

    def test_P2PKH_RawTx_SingleInput_SingleOutput(self):
        # Inputs
        prev_tx = "d53b66eea5c5ff7d8a2ab9b03187acca52538c861298f550727e87176a38241d"
        prev_address = "1NzXa3pE19AkomZHHUaxbV7LGxK8nMJpEa"
        prev_idx = 0

        # Outputs
        address = "1FmRHg4PQTiBAdnNmXneJRs1SCPR17uWW4"
        amount = 71943072

        expected = ("01000000011d24386a17877e7250f59812868c5352caac8731b0b92a8a7dffc5a"
                    "5ee663bd5000000001976a914f13bdea27f1fdfb164d083dd827ff55eb140d686"
                    "88acffffffff01a0c34904000000001976a914a1f856634fdac51ede71a2a1358"
                    "573556847078588ac00000000")

        tx_in = TransactionInput(prev_tx, prev_idx, prev_address, SpendType.P2PKH)
        tx_out = TransactionOutput(amount, address, SpendType.P2PKH)

        tx = Transaction()
        tx.add_inputs(tx_in)
        tx.add_outputs(tx_out)

        raw = tx.serialize()

        self.assertEqual(expected, raw.hex())

    def test_P2PKH_RawTx_SingleInput_SingleOutput_2(self):
        # Inputs
        prev_tx = "e220edf4ac210e74443cd28661d185d42664977151c277ed07a058ba07df24d4"
        prev_address = "16kb6Sy8eDeUpkiSr2DzjvZbtZ1kQtiCTK"
        prev_idx = 8

        # Outputs
        address = "1FmRHg4PQTiBAdnNmXneJRs1SCPR17uWW4"

        amount = 591117

        expected = ("0100000001d424df07ba58a007ed77c25171976426d485d16186d23c44740e21"
                    "acf4ed20e2080000001976a9143f16f9b73c09a678997c6e479efae2c0df6feb"
                    "9e88acffffffff010d050900000000001976a914a1f856634fdac51ede71a2a1"
                    "358573556847078588ac00000000")

        tx_in = TransactionInput(prev_tx, prev_idx, prev_address, SpendType.P2PKH)
        tx_out = TransactionOutput(amount, address, SpendType.P2PKH)

        tx = Transaction()
        tx.add_inputs(tx_in)
        tx.add_outputs(tx_out)

        raw = tx.serialize()

        self.assertEqual(expected, raw.hex())

    def test_P2PKH_RawTx_MultipleInput_SingleOutput(self):
        # Inputs
        prev_tx_1 = "8ab885867092db0d1a7220fc8bb0b549c156ea7bb69435a08161bdcbd8864f46"
        prev_idx_1 = 2
        prev_address_1 = "1Mvigy76bN9y55YisBY6YxkrTGkYWoDe3Y"
        value_1 = 91520573

        prev_tx_2 = "8d097c739096828989427f1a00910996fd14c6c2d322fd559e9b68ef43d25024"
        prev_idx_2 = 0
        prev_address_2 = "1Ak779xz5e2x5MM9mGRsPc3XLFjCUAEH3p"
        value_2 = 416110

        # Outputs
        address = "16Fg2yjwrbtC6fZp61EV9mNVKmwCzGasw5"
        amount = (value_1 + value_2) - 1

        expected = ("0100000002464f86d8cbbd6181a03594b67bea56c149b5b08bfc20721a0ddb927086"
                    "85b88a020000001976a914e58b5ca8dedf22a4e86ebfa3a6ac0a595abf887688acff"
                    "ffffff2450d243ef689b9e55fd22d3c2c614fd960991001a7f428989829690737c09"
                    "8d000000001976a9146ae01d93e035b5724748b427d9d565c18a44885a88acffffff"
                    "ff01aad77a05000000001976a914399f09529a1e7f37ff5a892644b47690ab5e516f"
                    "88ac00000000")

        tx_in_1 = TransactionInput(prev_tx_1, prev_idx_1, prev_address_1, SpendType.P2PKH)
        tx_in_2 = TransactionInput(prev_tx_2, prev_idx_2, prev_address_2, SpendType.P2PKH)
        tx_out = TransactionOutput(amount, address, SpendType.P2PKH)

        tx = Transaction()
        tx.add_inputs(tx_in_1, tx_in_2)
        tx.add_outputs(tx_out)

        raw = tx.serialize()

        self.assertEqual(expected, raw.hex())

    def test_MultipleInput_MultipleOutpute(self):
        # https://api.blockcypher.com/v1/btc/main/txs/b4c2edbe77af5ef1f69f91256fc84d0902037ead0bbe8f600b6c4d170afecfec?limit=50&includeHex=true
        # multiple inputs and multiple outputs, one p2pkh other p2sh
        prev_tx_1 = "5e2e877f7768a2a85018509776013242bc829a599c67a702f0a01b8815626a43"
        prev_idx_1 = 193
        prev_addr_1 = "15BRZw6jmoJesHBb9npiseHFawkkTQPin4"
        input_1 = TransactionInput(prev_tx_1, prev_idx_1, prev_addr_1, SpendType.P2PKH)

        prev_tx_2 = "4104e6d8de6518d30014c90ddb2af8912c36dfef928e8cae22df092c3e93d0b7"
        prev_idx_2 = 1
        prev_addr_2 = "1MZnPNbhtmRjzAHqEikQYB7ENaRd5ky4aT"
        input_2 = TransactionInput(prev_tx_2, prev_idx_2, prev_addr_2, SpendType.P2PKH)

        output1 = TransactionOutput(776443, "13UGKrszWSkJ1328g2ugy4xvTHjHTaf5ye", SpendType.P2PKH)
        output2 = TransactionOutput(15290595, "3QhnzCp56gUaaAw9VfVbstXm9JZoZVrEzP", SpendType.P2SH)

        tx = Transaction()
        tx.add_inputs(input_1, input_2)
        tx.add_outputs(output1, output2)

        expected_raw = ("0100000002436a6215881ba0f002a7679c599a82bc4232017697501850a8a268777f872e5ec1000000"
                        "1976a9142dd92bc1b62507a6e23bc685d4e3723486ce591388acffffffffb7d0933e2c09df22ae8c8e"
                        "92efdf362c91f82adb0dc91400d31865ded8e60441010000001976a914e195b669de8e49f955749033"
                        "fa2d79390732c43588acffffffff02fbd80b00000000001976a9141b18467d085f8aa44493a2d5f3cb"
                        "771ab5ae412588ace350e9000000000017a914fc708283a974bacd4b1bdbf1ac25a121baa291398700"
                        "000000")

        raw_tx = tx.serialize().hex()

        self.assertEqual(expected_raw, raw_tx)

    def test_sign_1(self):
        # Sign simple 1 input tx
        priv_k = PrivateKey(0x0ecd20654c2e2be708495853e8da35c664247040c00bd10b9b13e5e86e6a808d)
        pub_k = priv_k.create_pub_key()

        prev_tx = "96534da2f213367a6d589f18d7d6d1689748cd911f8c33a9aee754a80de166be"
        prev_address = "1MBngSqZbMydscpzSoehjP8kznMaHAzh9y"
        prev_idx = 0

        address = "1FromKBPAS8MWsk1Yv1Yiu8rJbjfVioBHc"
        amount = 118307

        tx = Transaction()
        tx.add_inputs(TransactionInput(prev_tx, prev_idx, prev_address, SpendType.P2PKH))
        tx.add_outputs(TransactionOutput(amount, address, SpendType.P2PKH))

        signed = tx.sign(KeyPair(priv_k, pub_k))

        expected = ("0100000001be66e10da854e7aea9338c1f91cd489768d1d6d7189f586d7a3613f2a24d539600000000"
                    "6b483045022100d26da559a61d0156429ee63e31d6b0502a662b8d0fc1a6eb269658ecd436c8aa0220"
                    "024e474c33b20f8adbcc36ddd01e24562c917ccc1a4b6f21cc7926099a9984c20121032daa93315eeb"
                    "be2cb9b5c3505df4c6fb6caca8b756786098567550d4820c09dbffffffff0123ce0100000000001976"
                    "a914a2fd2e039a86dbcf0e1a664729e09e8007f8951088ac00000000")

        self.assertEqual(expected, signed.serialize().hex())

    def test_sign_2(self):
        # Multiple P2PKH inputs and 1 P2PKH output
        priv_k = PrivateKey(0x22861a6e8a0670f6388847e83bbea3ed580280b612c11470998baf11ed95d032, compression=False)

        input1 = TransactionInput("2dac8856a21e3cd0fae25b28ef44c2ab4360fe3daa2fdc8815f89ad3b03c9486", 0,
                                  "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4",
                                  SpendType.P2PKH)

        input2 = TransactionInput("d53b66eea5c5ff7d8a2ab9b03187acca52538c861298f550727e87176a38241d", 0,
                                  "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4",
                                  SpendType.P2PKH)

        output = TransactionOutput(130000000 + 71941172, "mvHNaj9NDV9RwkFzV6m28M5LJBz7r5vNwQ", SpendType.P2PKH)

        expected = ("020000000286943cb0d39af81588dc2faa3dfe6043abc244ef285be2fad03c1ea25688ac2d000000008b483045"
                    "022100d72dd4a871d1db72d32ee3da5ad1349daa99d8b67567efcfd8c273f8b95ba3770220439542142cd966f4"
                    "67403a583397a5643128e203863349328d4a7c6822cf670e014104dc406568adadd693f302205af9694bf3caf3"
                    "da0374f2183bea4680fb0d1f5cf5f06c2a78a0229129023260658e4e9f37d7d9e22fad81dfdbb944163138a82b"
                    "68ffffffff1d24386a17877e7250f59812868c5352caac8731b0b92a8a7dffc5a5ee663bd5000000008b483045"
                    "022100923a2d1a56c90536a84575c5b459cd2e22345951f3840cb77810a88e9585a261022077595add75ffa707"
                    "bbdedd4ab952f0fb93add38f8e979d8e3fdacaaaf4c99a73014104dc406568adadd693f302205af9694bf3caf3"
                    "da0374f2183bea4680fb0d1f5cf5f06c2a78a0229129023260658e4e9f37d7d9e22fad81dfdbb944163138a82b"
                    "68ffffffff01b460090c000000001976a914a1f856634fdac51ede71a2a1358573556847078588ac00000000")

        tx = Transaction(version=2)
        tx.add_inputs(input1, input2)
        tx.add_outputs(output)

        signed = tx.sign(KeyPair(priv_k, priv_k.create_pub_key()))

        serialize__hex = signed.serialize().hex()
        self.assertEqual(expected, serialize__hex)

    def test_sign_3(self):
        # Test spending a P2PKH input to a P2WPKH
        priv_k = PrivateKey(0x95fa16fb03e27b77166b6a0e03493eda7ad06a64a273f8ddb82238141a1b59dd)

        input = TransactionInput("53ca9780e8c7a0022e2146477433eac26be5b27ef2b0ba969f6431b92a2b4108", 0,
                                 "mvHNaj9NDV9RwkFzV6m28M5LJBz7r5vNwQ",
                                 SpendType.P2PKH)

        output = TransactionOutput(201921172, "tb1qfeytr2u0d3e3tny5kyjvjule3srx33eclcx6sy", SpendType.P2WPKH)

        tx = Transaction(version=2)
        tx.add_inputs(input)
        tx.add_outputs(output)

        expected_raw = ("020000000108412b2ab931649f96bab0f27eb2e56bc2ea33744746212e02a0c7e88097ca5300000000"
                        "1976a914a1f856634fdac51ede71a2a1358573556847078588acffffffff019412090c000000001600"
                        "144e48b1ab8f6c7315cc94b124c973f98c0668c73800000000")

        self.assertEqual(expected_raw, tx.serialize().hex())

        signed = tx.sign(KeyPair(priv_k, priv_k.create_pub_key()))

        expected_signed = ("020000000108412b2ab931649f96bab0f27eb2e56bc2ea33744746212e02a0c7e88097ca530000000"
                           "06b4830450221008154ea4ed4c96f8076e10734a3e507f8b183e784e8578c4dde648536b1d0723f02"
                           "20158963e8d4d8ff47ff288b51ce250b561f08e08bc3f97691b00da5f3d1bf334f01210320c617efd"
                           "2de9208533c0deecc38610fc33cd3f7dd9e9b107f3b87cd7cdc3a21ffffffff019412090c00000000"
                           "1600144e48b1ab8f6c7315cc94b124c973f98c0668c73800000000")

        serialize__hex = signed.serialize().hex()
        self.assertEqual(expected_signed, serialize__hex)

    def test_sign_4(self):
        # P2PK + P2WPKH inputs -> P2PKH outputs
        # See https://github.com/bitcoin/bips/blob/master/bip-0143.mediawiki

        tx_input_1 = TransactionInput("9f96ade4b41d5433f4eda31e1738ec2b36f6e7d1420d94a6af99801a88f7f7ff", 0,
                                      "03c9f4836b9a4f77fc0d81f7bcb01b7f1b35916864b9476c241ce9fc198bd25432",
                                      SpendType.P2PK, sequence=b'\xff\xff\xff\xee')
        priv_k1 = PrivateKey(0xbbc27228ddcb9209d7fd6f36b02f7dfa6252af40bb2f1cbc7a557da8027ff866)
        pub_k1 = priv_k1.create_pub_key()

        tx_input_2 = TransactionInput("8ac60eb9575db5b2d987e29f301b5b819ea83a5c6579d282d189cc04b8e151ef", 1,
                                      "tb1qr583w2swedy2acd7rung055k8t3n7udp52l3lm",
                                      SpendType.P2WPKH, prev_amount=6)
        priv_k2 = PrivateKey(0x619c335025c7f4012e556c2a58b2506e30b8511b53ade95ea316fd8c3286feb9)
        pub_k2 = PublicKey(binascii.unhexlify("025476c2e83188368da1ff3e292e7acafcdb3566bb0ad253f62fc70f07aeee6357"))

        tx_output_1 = TransactionOutput(112340000, "msQzKJatdWdw4rpy8sbv8puHoncseekYCf", SpendType.P2PKH)
        tx_output_2 = TransactionOutput(223450000, "mkyWRMBNtjzZxdCcEZDYNi5CSoYnRaKACc", SpendType.P2PKH)

        tx = Transaction(lock_time=17)
        tx.add_inputs(tx_input_1, tx_input_2)
        tx.add_outputs(tx_output_1, tx_output_2)

        expected_raw = ("0100000002fff7f7881a8099afa6940d42d1e7f6362bec38171ea3edf433541db4e4ad969f00000000"
                        "232103c9f4836b9a4f77fc0d81f7bcb01b7f1b35916864b9476c241ce9fc198bd25432aceeffffffef"
                        "51e1b804cc89d182d279655c3aa89e815b1b309fe287d9b2b55d57b90ec68a010000001600141d0f17"
                        "2a0ecb48aee1be1f2687d2963ae33f71a1ffffffff02202cb206000000001976a9148280b37df378db"
                        "99f66f85c95a783a76ac7a6d5988ac9093510d000000001976a9143bde42dbee7e4dbe6a21b2d50ce2"
                        "f0167faa815988ac11000000")

        self.assertEqual(expected_raw, tx.serialize().hex())

        expected_signed = ("01000000000102fff7f7881a8099afa6940d42d1e7f6362bec38171ea3edf433541db4e4ad969f00"
                           "000000494830450221008b9d1dc26ba6a9cb62127b02742fa9d754cd3bebf337f7a55d114c8e5cdd"
                           "30be022040529b194ba3f9281a99f2b1c0a19c0489bc22ede944ccf4ecbab4cc618ef3ed01eeffff"
                           "ffef51e1b804cc89d182d279655c3aa89e815b1b309fe287d9b2b55d57b90ec68a0100000000ffff"
                           "ffff02202cb206000000001976a9148280b37df378db99f66f85c95a783a76ac7a6d5988ac909351"
                           "0d000000001976a9143bde42dbee7e4dbe6a21b2d50ce2f0167faa815988ac000247304402203609"
                           "e17b84f6a7d30c80bfa610b5b4542f32a8a0d5447a12fb1366d7f01cc44a0220573a954c45183315"
                           "61406f90300e8f3358f51928d43c212a8caed02de67eebee0121025476c2e83188368da1ff3e292e"
                           "7acafcdb3566bb0ad253f62fc70f07aeee635711000000")

        signed = tx.sign(KeyPair(priv_k1, pub_k1), KeyPair(priv_k2, pub_k2))

        self.assertEqual(expected_signed, signed.serialize().hex())

    def test_sign_5(self):
        tx_input_1 = TransactionInput("b9b72078c53511dfdb80ba91e04696cfe479b320a2dfc17a96be40ce2884a62f", 0,
                                      "tb1qfeytr2u0d3e3tny5kyjvjule3srx33eclcx6sy",
                                      SpendType.P2WPKH, 0.99996220)
        priv_k1 = PrivateKey.from_wif("cVZiWLak3RfzgFZtLeZ87TKnFwaG1hBgxovNmv9XwmaSSrNLXKp1")
        pub_k1 = priv_k1.create_pub_key()

        tx_output_1 = TransactionOutput(99994220, "n3WUs6uCpAc1at2u13ZLRQKf8wuqgVdZr4", SpendType.P2PKH)

        tx = Transaction()
        tx.add_inputs(tx_input_1)
        tx.add_outputs(tx_output_1)

        signed = tx.sign(KeyPair(priv_k1, pub_k1))

        expected_signed = ("010000000001012fa68428ce40be967ac1dfa220b379e4cf9646e091ba80dbdf1135c57820b7b90000000000"
                           "ffffffff016ccaf505000000001976a914f13bdea27f1fdfb164d083dd827ff55eb140d68688ac0248304502"
                           "2100fd3e612284f6d107fcb40d8dad1d7d57ac570fe11116a7f61fb80f5905e4124e0220102c75534b37a9f3"
                           "b82fc42994bc35aa07f1ec9113e34b7d8489dc0c8bbbeb5a0121037c32fea2feddc1b8a500ec4ff9b597dc72"
                           "d237ed205aa395704035172d74a05c00000000")

        self.assertEqual(expected_signed, signed.serialize().hex())

    @staticmethod
    def to_int(b):
        return int.from_bytes(b, 'big')


if __name__ == '__main__':
    unittest.main()
