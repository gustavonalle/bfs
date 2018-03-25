from lib.spender import Spender
from lib.transaction import Sign, Enum


class BCISpender(Spender):

    def __init__(self):
        super().__init__()
        self.tx_version = 2
        self.sig_hash_type = 0x41
        self.sig_hash_type_pre_image = self.sig_hash_type | (79 << 8)
        self.sign_type = Sign.SEGWIT


class BCINetwork(Enum):
    MAIN_NET = b'\x66'
    TEST_NET = b'\x6f'
