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
    def remove_leading_zeroes(b):
        b = b.lstrip(b'\x00')
        if b[0] & 0x80:
            b = b'\x00' + b
        return b

    @staticmethod
    def der(ecdsa):
        r = ecdsa[0].to_bytes(32, 'big')
        s = ecdsa[1].to_bytes(32, 'big')

        r = Encoder.remove_leading_zeroes(r)
        s = Encoder.remove_leading_zeroes(s)

        payload = b'\x02' + Encoder.with_size(r) + b'\x02' + Encoder.with_size(s)
        return b'\x30' + Encoder.with_size(payload)
