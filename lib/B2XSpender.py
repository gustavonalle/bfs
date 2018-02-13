from lib.spender import Spender


class B2XSpender(Spender):

    def __init__(self):
        super().__init__()
        self.tx_version = 1
        self.sig_hash_type = 0x21
