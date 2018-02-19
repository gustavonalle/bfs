from unittest import TestCase

from lib.B2XSpender import B2XSpender
from lib.keys import PrivateKey
from lib.spender import Utxo, Destination


class TestB2XSpender(TestCase):

    def test_send_to_bech32(self):
        # Generated with regtest
        pk = PrivateKey.from_wif("cVQ1cnAfsQPAexvQwSTD2Yqeoofr34aNjuLPjQsvcyXsSMcxc5eZ")

        utxo = Utxo("fba837c65dcade7332d6dc54826cd4f4de402a07a13c01889a940e91fcbb0e86", 0,
                    "mqbqnHixVLLpT4p2pzdGPuYQsj5n9JPF5U", 49.99990000, pk)

        spender = B2XSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(49.99980000, "tb1qcydtudnm69tss5daad459rv8qaee485cux9vev"))

        tx_hex = spender.create_tx().hex()

        expected = ("0200000001860ebbfc910e949a88013ca1072a40def4d46c8254dcd63273deca5dc637a8fb000000006a4730440"
                    "22040dcd2952802af9dd9add4c02c82104f356acf848e2679d49e2b48d1f68815ea02201d1d97bd27604fb8c720"
                    "514f98abc1436eefa1390df622ea9ac822c78328c24321210231cad08d94f860b4dcf9ef717544946c70dad4d22"
                    "e8c569a2c8da287834f39aaffffffff01e0a3052a01000000160014c11abe367bd1570851bdeb6b428d8707739a"
                    "9e9800000000")

        self.assertEqual(expected, tx_hex)

    def test_spend_p2pkh(self):
        # Generated with regtest
        pk = PrivateKey.from_wif("cVhpUkwh5Nboa1ZX9N8XuBAWXQuFUNAoPhYegUBuEbSPzYfgxS2C")

        utxo = Utxo("ff8e86772fa46e8ec35d40592c59a6320d32d499c4f1e393a5d2ab611334e508", 0,
                    "mjrhteDrywvuQerJCmCGfuTSdZoEea54Jo", 50, pk)

        spender = B2XSpender()
        spender.add_utxos(utxo)
        spender.add_destinations(Destination(49.9999, "mqbqnHixVLLpT4p2pzdGPuYQsj5n9JPF5U"))

        tx_hex = spender.create_tx().hex()

        expected = ("020000000108e5341361abd2a593e3f1c499d4320d32a6592c59405dc38e6ea42f77868eff00000000"
                    "6a4730440220630327d0f0b55285640075c8eaea439adebdc0713bad32469bdb73b8d18e5fe7022066"
                    "3329830183c8f6522681d38be7a12696dc926fe0bf31b3abed2f33cc41b64b212102f2717a40c42c69"
                    "1bbe291a58c8c43877e170319c4eee18f9140557c5632e35deffffffff01f0ca052a010000001976a9"
                    "146e9de6950a429d009c08a35f731fd7896baecf9588ac00000000")

        self.assertEqual(expected, tx_hex)
