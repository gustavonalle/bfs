from lib.spender import Spender


class BTVSpender(Spender):

    def __init__(self):
        super().__init__()
        self.tx_version = 2
        self.sig_hash_type = 0x41
        self.sig_hash_type_pre_image = self.sig_hash_type | (50 << 8)
