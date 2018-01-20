import hashlib
import itertools
import secrets
from enum import Enum


class AddressType(Enum):
    MAIN_NET = b'\x00'
    TEST_NET = b'\x6f'


MAX_PRIVATE_KEY_VALUE = 1.158 * 10 ** 77
BASE58_DIGITS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


# https://en.bitcoin.it/wiki/Base58Check_encoding
def create_address_v1(n, address_type):
    step1 = address_type.value + n
    step2 = double_sha256(step1)
    step3 = step2[0:4]
    step4 = step1 + step3
    return base58_encode(step4)


def hash160_from_address(address):
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


def double_sha256(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def generate_random(nbits):
    key = secrets.randbits(nbits)
    if key < MAX_PRIVATE_KEY_VALUE:
        return key
    else:
        return generate_random(nbits)
