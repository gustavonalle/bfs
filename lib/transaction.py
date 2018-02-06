import binascii
import copy

from lib.address import Bech32Address
from lib.commons import *
from lib.elliptic import Curve


class TransactionInput(object):

    def __init__(self, prev_tx_hash, index, address, spend_type, prev_amount=0, sequence=b'\xFF\xFF\xFF\xFF'):
        self.prev_amount = prev_amount
        self.prevTxHash = prev_tx_hash
        self.index = index
        self.address = address
        self.spendType = spend_type
        if self.spendType == SpendType.P2PKH:
            self.pub_key_or_hash = hash160_from_address(self.address, spend_type)
        elif self.spendType == SpendType.P2PK:
            self.pub_key_or_hash = binascii.unhexlify(address)
        elif self.spendType == SpendType.P2WPKH:
            self.pub_key_or_hash = Bech32Address.from_address(address).hash160
            if self.prev_amount == 0:
                raise RuntimeError("UTXO amount must be provided for P2WPKH Inputs")
        else:
            raise RuntimeError("spend type not supported:" + self.spendType)
        self.prev_script = Script.script_pub_key(self.pub_key_or_hash, self.spendType)
        self.sequence = sequence

    def serialize(self):
        payload = binascii.unhexlify(self.prevTxHash)[::-1]
        payload += self.index.to_bytes(4, 'little')
        payload += to_bytes_with_size(self.prev_script)
        payload += self.sequence[::-1]
        return payload

    def serialize_prev_amount(self):
        satoshis = btc_to_satoshis(self.prev_amount)
        return satoshis.to_bytes(8, 'little')

    def serialize_prev_out(self):
        payload = binascii.unhexlify(self.prevTxHash)[::-1]
        payload += self.index.to_bytes(4, 'little')
        return payload


class Script(object):
    OP_0 = b'\x00'
    OP_CHECKSIG = b'\xac'
    OP_DUP = b'\x76'
    OP_EQUAL = b'\x87'
    OP_EQUALVERIFY = b'\x88'
    OP_HASH160 = b'\xa9'

    @staticmethod
    def script_pub_key(pub_key_or_hash, spend_type):
        hash_with_size = to_bytes_with_size(pub_key_or_hash)
        if spend_type == SpendType.P2PKH:
            return Script.OP_DUP + Script.OP_HASH160 + hash_with_size + Script.OP_EQUALVERIFY + Script.OP_CHECKSIG
        if spend_type == SpendType.P2SH:
            return Script.OP_HASH160 + hash_with_size + Script.OP_EQUAL
        if spend_type == SpendType.P2WPKH:
            return Script.OP_0 + hash_with_size
        if spend_type == SpendType.P2PK:
            return hash_with_size + Script.OP_CHECKSIG
        raise RuntimeError("Invalid spend type " + spend_type)


class TransactionOutput(object):

    def __init__(self, satoshis, address, spend_type):
        self.satoshis = satoshis
        self.address = address
        self.spendType = spend_type
        self.hash160 = hash160_from_address(address, spend_type)

    def lock_script(self):
        return Script.script_pub_key(self.hash160, self.spendType)

    def serialize(self):
        amount = self.satoshis.to_bytes(8, 'little')
        script = self.lock_script()
        return amount + to_bytes_with_size(script)


class Transaction(object):
    elliptic = Curve()
    marker = b'\x00'
    flag = b'\x01'

    def __init__(self, version=1, lock_time=0):
        self.version = version
        self.inputs = list()
        self.outputs = list()
        self.lock_time = lock_time
        self.witness = b''

    def add_inputs(self, *tx_inputs):
        for i in tx_inputs:
            self.inputs.append(i)

    def add_outputs(self, *tx_outputs):
        for o in tx_outputs:
            self.outputs.append(o)

    def serialize_segwit(self):
        payload = self.version.to_bytes(4, 'little')
        payload += self.marker
        payload += self.flag
        payload += to_varint(len(self.inputs))
        for i in self.inputs:
            payload += i.serialize()
        payload += to_varint(len(self.outputs))
        for o in self.outputs:
            payload += o.serialize()
        payload += self.witness
        payload += int.to_bytes(self.lock_time, 4, 'little')
        return payload

    def serialize_legacy(self, with_hash_code=False):
        payload = self.version.to_bytes(4, 'little')
        payload += to_varint(len(self.inputs))
        for i in self.inputs:
            payload += i.serialize()
        payload += to_varint(len(self.outputs))
        for o in self.outputs:
            payload += o.serialize()
        payload += int.to_bytes(self.lock_time, 4, 'little')
        if with_hash_code:
            payload += (1).to_bytes(4, 'little')
        return payload

    def serialize(self, with_hash_code=False):
        if self.witness == b'':
            return self.serialize_legacy(with_hash_code)
        return self.serialize_segwit()

    def hash_prev_outs(self):
        prev_outs = b''
        for i in self.inputs:
            prev_outs += i.serialize_prev_out()
        return double_sha256(prev_outs)

    def hash_prev_seq(self):
        prev_outs = b''
        for i in self.inputs:
            prev_outs += i.sequence[::-1]
        return double_sha256(prev_outs)

    def hash_outputs(self):
        outputs = b''
        for o in self.outputs:
            outputs += o.serialize()
        return double_sha256(outputs)

    def create_pre_image_segwit(self, idx_input):
        segwit_input = self.inputs[idx_input]
        if segwit_input.spendType != SpendType.P2WPKH:
            raise RuntimeError("Input must be P2WPKH")
        payload = self.version.to_bytes(4, 'little')
        payload += self.hash_prev_outs()
        payload += self.hash_prev_seq()
        payload += segwit_input.serialize_prev_out()
        payload += to_bytes_with_size(Script.script_pub_key(segwit_input.pub_key_or_hash, spend_type=SpendType.P2PKH))
        payload += segwit_input.serialize_prev_amount()
        payload += segwit_input.sequence[::-1]
        payload += self.hash_outputs()
        payload += int.to_bytes(self.lock_time, 4, 'little')
        payload += (1).to_bytes(4, 'little')
        return payload

    def create_pre_image_legacy(self, idx_input):
        template = copy.deepcopy(self)
        template.erase_input_scripts(idx_input)
        return template.serialize(with_hash_code=True)

    @classmethod
    def is_segwit(cls, tx_input):
        return tx_input.spendType == SpendType.P2WPKH

    def sign(self, *key_pairs):
        witnesses = list()
        signed_tx = copy.deepcopy(self)
        has_witness = False

        key_pair_size = len(key_pairs)
        if key_pair_size == 0:
            raise RuntimeError("Must provide a list of KeyPair in order to sign!")

        for i, tx_input in enumerate(self.inputs):
            if i > key_pair_size - 1:
                key_pair = key_pairs[0]
            else:
                key_pair = key_pairs[i]
            private_key = key_pair.priv_key
            public_key = key_pair.pub_key
            raw = self.pre_image(i)
            dhash = double_sha256(raw)
            signature = self.elliptic.ecdsa(private_key.key, dhash)
            der_sig = der(signature) + b'\x01'
            script_sig = to_bytes_with_size(der_sig)
            if tx_input.spendType != SpendType.P2PK:
                script_sig += to_bytes_with_size(public_key.key)
            signed_input = copy.deepcopy(tx_input)
            if not self.is_segwit(tx_input):
                witnesses.append(b'\x00')
                signed_input.prev_script = script_sig
            else:
                has_witness = True
                witnesses.append(b'\x02' + script_sig)
                signed_input.prev_script = None
            signed_tx.replace_input(i, signed_input)

        if has_witness:
            for w in witnesses:
                signed_tx.witness += w

        return signed_tx

    def replace_input(self, i, signed_input):
        self.inputs[i] = signed_input

    def erase_input_scripts(self, except_id):
        for i, tx_input in enumerate(self.inputs):
            if i != except_id:
                tx_input.prev_script = None

    def pre_image(self, i):
        if self.is_segwit(self.inputs[i]):
            return self.create_pre_image_segwit(i)
        return self.create_pre_image_legacy(i)
