from enum import Enum


class SpendType(Enum):
    P2PKH = 0
    P2WPKH = 1


class Encoder(object):

    @staticmethod
    def to_varint(n):
        if n <= 0xfc:
            return n.to_bytes(1, 'little')
        if n <= 0xffff:
            return b'\xfd' + n.to_bytes(2, 'little')
        if n <= 0xffffffff:
            return b'\xfe' + n.to_bytes(4, 'little')
        if n <= 0xffffffffffffffff:
            return b'\xff' + n.to_bytes(8, 'little')


class TransactionInput(object):

    def __init__(self, prev_tx_hash, index, spend_type):
        self.prevTxHash = prev_tx_hash
        self.index = index
        self.spendType = spend_type


class Opcode(Enum):
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
        if self.spendType == SpendType.P2PKH:
            hash_bytes = self.hash160.to_bytes(20, 'big')
            hash_size = self.size(hash_bytes)
            return Opcode.OP_DUP.value + Opcode.OP_HASH160.value + hash_size + hash_bytes + Opcode.OP_EQUALVERIFY.value + Opcode.OP_CHECKSIG.value

    @staticmethod
    def size(content):
        s = len(content)
        return Encoder.to_varint(s)

    def serialize(self):
        amount = self.satoshis.to_bytes(8, 'little')
        script = self.lock_script()
        return amount + self.size(script) + script
