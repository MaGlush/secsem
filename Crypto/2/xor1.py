from itertools import cycle


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def xor(message, key):
    return bytes(a^b for a, b in zip(message, cycle(key)))


key = b'key'
xor('hello world'.encode(), key)