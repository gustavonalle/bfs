import hashlib
import itertools

BASE58_DIGITS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


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
    size = len(content)
    return to_varint(size) + content


def remove_leading_zeroes(b):
    b = b.lstrip(b'\x00')
    if b[0] & 0x80:
        b = b'\x00' + b
    return b


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


def der(ecdsa):
    r = ecdsa[0].to_bytes(32, 'big')
    s = ecdsa[1].to_bytes(32, 'big')

    r = remove_leading_zeroes(r)
    s = remove_leading_zeroes(s)

    payload = b'\x02' + to_bytes_with_size(r) + b'\x02' + to_bytes_with_size(s)
    return b'\x30' + to_bytes_with_size(payload)
