from enum import Enum
from lib.utils import Encoder


class SpendType(Enum):
    P2PKH = 0
    P2WPKH = 1


class TransactionInput(object):

    def __init__(self, prev_tx_hash, index, spend_type):
        self.prevTxHash = prev_tx_hash
        self.index = index
        self.spendType = spend_type


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

    def lock_script(self):
        hash_bytes = self.hash160.to_bytes(20, 'big')
        payload = Encoder.with_size(hash_bytes)
        if self.spendType == SpendType.P2PKH:
            return Script.OP_DUP + Script.OP_HASH160 + payload + Script.OP_EQUALVERIFY + Script.OP_CHECKSIG
        if self.spendType == SpendType.P2WPKH:
            return Script.OP_0 + payload

    def serialize(self):
        amount = self.satoshis.to_bytes(8, 'little')
        script = self.lock_script()
        return amount + Encoder.with_size(script)
