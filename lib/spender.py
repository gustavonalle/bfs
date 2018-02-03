from lib.commons import btc_to_satoshis
from lib.keys import KeyPair
from lib.transaction import Transaction, TransactionInput, TransactionOutput, SpendType


class Utxo(object):

    def __init__(self, tx_hash, index, address, amount_btc):
        self.amount_btc = amount_btc
        self.address = address
        self.index = index
        self.tx_hash = tx_hash


class Destination(object):

    def __init__(self, amount_btc, address):
        self.address = address
        self.amount_btc = amount_btc


class Spender(object):

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

    def create_p2pkh_tx(self, private_key):
        tx = Transaction()

        for utxo in self.utxos:
            tx_input = TransactionInput(utxo.tx_hash, utxo.index, utxo.address, SpendType.P2PKH)
            tx.add_inputs(tx_input)

        for destination in self.destinations:
            tx_output = TransactionOutput(btc_to_satoshis(destination.amount_btc), destination.address, SpendType.P2PKH)
            tx.add_outputs(tx_output)

        public_key = private_key.create_pub_key()
        signed = tx.sign(KeyPair(private_key, public_key))
        return signed.serialize()
