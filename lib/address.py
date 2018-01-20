from enum import Enum

from lib.utils import double_sha256, base58_encode


class AddressType(Enum):
    MAIN_NET = b'\x00'
    TEST_NET = b'\x6f'


# https://en.bitcoin.it/wiki/Base58Check_encoding
def create_address_v1(n, address_type):
    step1 = address_type.value + n
    step2 = double_sha256(step1)
    step3 = step2[0:4]
    step4 = step1 + step3
    return base58_encode(step4)
