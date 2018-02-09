import hashlib
import itertools
import math
from enum import Enum

from lib.bech32 import decode

BASE58_DIGITS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


class SpendType(Enum):
    P2PK = 0
    P2PKH = 1
    P2SH = 2
    P2WPKH = 3
    P2SH_P2WPKH = 4


class Network(Enum):
    MAIN_NET = b'\x00'
    TEST_NET = b'\x6f'


class HashType(Enum):
    SIG_HASH_ALL = b'\x01'


def get_spend_type(address):
    if address.startswith("tb1") or address.startswith("bc1"):
        return SpendType.P2WPKH
    if address.startswith("3") or address.startswith("2"):
        return SpendType.P2SH_P2WPKH
    return SpendType.P2PKH


def to_varint(n):
    if n <= 0xfc:
        return n.to_bytes(1, 'little')
    if n <= 0xffff:
        return b'\xfd' + n.to_bytes(2, 'little')
    if n <= 0xffffffff:
        return b'\xfe' + n.to_bytes(4, 'little')
    if n <= 0xffffffffffffffff:
        return b'\xff' + n.to_bytes(8, 'little')


def to_bytes_with_size(content):
    if content is None:
        return b'\x00'
    else:
        size = len(content)
        return to_varint(size) + content


def remove_leading_zeroes(b):
    b = b.lstrip(b'\x00')
    if b[0] & 0x80:
        b = b'\x00' + b
    return b


def hash160_from_address(address, spend_type):
    if spend_type == SpendType.P2WPKH:
        hrp, data = decode(address[0:2], address)
        return bytes(data)
    else:
        h = base58_decode(address)
        b = h.to_bytes(25, 'big')[1:-4]
        return b


def base58_decode(base58):
    n = 0
    for d in base58:
        n = 58 * n + BASE58_DIGITS.index(d)
    return n


def base58_encode(b):
    payload = int.from_bytes(b, 'big')
    res = ''
    while payload > 0:
        (payload, r) = divmod(payload, 58)
        res += BASE58_DIGITS[r]
    for _ in itertools.takewhile(lambda x: x == 0, b):
        res += BASE58_DIGITS[0]
    return res[::-1]


def sha256(b):
    return hashlib.sha256(b).digest()


def double_sha256(b):
    return sha256(sha256(b))


def from_wif(wif):
    start = wif[0]
    compressed = False
    if start == "L" or start == "K" or start == "c" or start == "9":
        compressed = True
    decoded = base58_decode(wif)
    b = decoded.to_bytes(decoded.bit_length() // 8, 'big')
    if compressed:
        b = b[1:-5]
    else:
        b = b[1:-4]
    return int.from_bytes(b, 'big')


def to_wif(b, network, compressed=False):
    prefix = b'\x80'
    if network == Network.TEST_NET:
        prefix = b'\xef'
    wif = prefix + b
    if compressed:
        wif += b'\x01'
    checksum = double_sha256(wif)[0:4:]
    wif += checksum
    return base58_encode(wif)


def btc_to_satoshis(btc):
    return math.ceil(btc * 1e8)


def satoshis_to_btc(satoshis):
    return satoshis / 1e8


def der(ecdsa):
    r = ecdsa[0].to_bytes(32, 'big')
    s = ecdsa[1].to_bytes(32, 'big')

    r = remove_leading_zeroes(r)
    s = remove_leading_zeroes(s)

    payload = b'\x02' + to_bytes_with_size(r) + b'\x02' + to_bytes_with_size(s)
    return b'\x30' + to_bytes_with_size(payload)
