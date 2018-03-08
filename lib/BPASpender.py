from enum import Enum

from lib.spender import Spender
from lib.transaction import Sign


class BPASpender(Spender):

    def __init__(self):
        super().__init__()
        self.tx_version = 2
        self.sig_hash_type = 33
        self.sig_hash_type_pre_image = self.sig_hash_type | (47 << 8)
        self.sign_type = Sign.SEGWIT


class BPANetwork(Enum):
    MAIN_NET = b'\x37'
    TEST_NET = b'\x6f'
