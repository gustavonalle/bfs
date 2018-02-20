from lib.spender import Spender


class B2XSpender(Spender):

    def __init__(self):
        super().__init__()
        self.tx_version = 2
        self.sig_hash_type = 0x21 | 0x10
        self.sig_hash_type_pre_image = self.sig_hash_type << 1
