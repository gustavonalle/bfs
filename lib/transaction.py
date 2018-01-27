import binascii
import copy

from lib.commons import *
from lib.elliptic import Curve


class SpendType(Enum):
    P2PKH = 0
    P2WPKH = 1


class TransactionInput(object):

    def __init__(self, prev_tx_hash, index, prev_script, spend_type):
        self.prevTxHash = prev_tx_hash
        self.index = index
        self.prev_script = prev_script
        self.spendType = spend_type

    def serialize(self):
        payload = binascii.unhexlify(self.prevTxHash)[::-1]
        payload += self.index.to_bytes(4, 'little')
        payload += to_bytes_with_size(self.unlock_script())
        payload += b'\xFF\xFF\xFF\xFF'
        return payload

    def unlock_script(self):
        return binascii.unhexlify(self.prev_script)


class Script(object):
    OP_0 = b'\x00'
    OP_CHECKSIG = b'\xac'
    OP_DUP = b'\x76'
    OP_EQUALVERIFY = b'\x88'
    OP_HASH160 = b'\xa9'


class TransactionOutput(object):

    def __init__(self, satoshis, hash160, spend_type):
        self.satoshis = satoshis
        self.hash160 = hash160
        self.spendType = spend_type
        self.index = 0
        self.tx = None

    def lock_script(self):
        hash_bytes = self.hash160.to_bytes(20, 'big')
        payload = to_bytes_with_size(hash_bytes)
        if self.spendType == SpendType.P2PKH:
            return Script.OP_DUP + Script.OP_HASH160 + payload + Script.OP_EQUALVERIFY + Script.OP_CHECKSIG
        if self.spendType == SpendType.P2WPKH:
            return Script.OP_0 + payload

    def serialize(self):
        amount = self.satoshis.to_bytes(8, 'little')
        script = self.lock_script()
        return amount + to_bytes_with_size(script)


class Transaction(object):
    elliptic = Curve()

    def __init__(self, version=1):
        self.version = version
        self.inputs = list()
        self.outputs = list()

    def add_inputs(self, *tx_inputs):
        for i in tx_inputs:
            self.inputs.append(i)

    def add_outputs(self, *tx_outputs):
        for index, o in enumerate(tx_outputs):
            self.outputs.append(o)
            o.tx = self
            o.index = index

    def serialize(self, with_hash_code=False):
        payload = self.version.to_bytes(4, 'little')
        payload += to_varint(len(self.inputs))
        for i in self.inputs:
            payload += i.serialize()
        payload += to_varint(len(self.outputs))
        for o in self.outputs:
            payload += o.serialize()
        payload += b'\x00' * 4
        if with_hash_code:
            payload += (1).to_bytes(4, 'little')
        return payload

    def sign(self, private_key, public_key):
        signed_tx = copy.deepcopy(self)
        for i, tx_input in enumerate(self.inputs):
            raw = self.serialize(with_hash_code=True)
            dhash = double_sha256(raw)
            signature = self.elliptic.ecdsa(private_key.key, public_key.point, dhash)
            der_sig = der(signature) + b'\x01'
            script_sig = to_bytes_with_size(der_sig) + to_bytes_with_size(public_key.get_value())
            signed_input = copy.deepcopy(tx_input)
            signed_input.prev_script = script_sig.hex()
            signed_tx.replace_input(i, signed_input)
        return signed_tx

    def replace_input(self, i, signed_input):
        self.inputs[i] = signed_input
