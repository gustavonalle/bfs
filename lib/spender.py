from lib.commons import btc_to_satoshis, get_spend_type
from lib.keys import KeyPair
from lib.transaction import Transaction, TransactionInput, TransactionOutput, Sign


class Utxo(object):

    def __init__(self, tx_hash, index, address, amount_btc, private_key):
        self.private_key = private_key
        self.amount_btc = amount_btc
        self.address = address
        self.index = index
        self.tx_hash = tx_hash


class Destination(object):

    def __init__(self, amount_btc, address):
        self.address = address
        self.amount_btc = amount_btc


class Spender(object):
    tx_version = 2
    sig_hash_type = 0x1
    sig_hash_type_pre_image = 0x1
    sign_type = Sign.AUTO

    def __init__(self):
        self.utxos = list()
        self.destinations = list()

    def add_utxos(self, *utxos):
        for utxo in utxos:
            self.utxos.append(utxo)

    def add_destinations(self, *destinations):
        for destination in destinations:
            self.destinations.append(destination)

    def validate(self):
        total_spend = sum([x.amount_btc for x in self.destinations])
        total_available = sum([x.amount_btc for x in self.utxos])
        if total_spend > total_available:
            raise RuntimeError("Cannot spend more than it's available in the UTXO(s)")

        if total_spend == total_available:
            raise RuntimeError("No room for fee!")

        fee = total_available - total_spend

        if fee > total_spend * 0.1:
            raise RuntimeError("Fee is larger than 10% of the amount to spend!")

    def create_tx(self):
        tx = Transaction(version=self.tx_version, sig_hash_type=self.sig_hash_type,
                         sig_hash_type_pre_image=self.sig_hash_type_pre_image, sign_style=self.sign_type)
        keys = []
        for utxo in self.utxos:
            pub_key = utxo.private_key.create_pub_key()
            keys.append(KeyPair(utxo.private_key, pub_key))
            tx_input = TransactionInput(utxo.tx_hash, utxo.index, utxo.address, get_spend_type(utxo.address),
                                        prev_amount=utxo.amount_btc, pub_key=pub_key)
            tx.add_inputs(tx_input)

        for destination in self.destinations:
            tx_output = TransactionOutput(btc_to_satoshis(destination.amount_btc), destination.address,
                                          get_spend_type(destination.address))
            tx.add_outputs(tx_output)

        signed = tx.sign(*keys)
        return signed.serialize()
