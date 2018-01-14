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

    @staticmethod
    def with_size(content):
        size = len(content)
        return Encoder.to_varint(size) + content

    @staticmethod
    def der(ecdsa, sig_hash):
        int_value = b'\x02'
        r = ecdsa[0].to_bytes(33, 'big')
        s = ecdsa[1].to_bytes(33, 'big')
        payload = int_value + Encoder.with_size(r) + int_value + Encoder.with_size(s) + sig_hash
        return b'\x30' + Encoder.with_size(payload)
