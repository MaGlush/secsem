import gmpy2
gmpy2.get_context().precision = 4096

from Crypto.PublicKey import RSA
from gmpy2 import root

CIPHER = ".enc"
MODULUS = ".pub.pem"
NUM = 5


def chinese_remainder_theorem(c, m):
    N = 1
    for n in m:
        N *= n
    items = []
    for i in range(len(c)):
        items.append((c[i],m[i]))
    result = 0
    for a, n in items:
        m = N // n
        r, s, d = extended_gcd(n, m)
        if d != 1:
            raise "Input not pairwise co-prime"
        result += a * s * m

    return result % N


def extended_gcd(a, b):
    x, y = 0, 1
    lastx, lasty = 1, 0

    while b:
        a, (q, b) = b, divmod(a, b)
        x, lastx = lastx - q * x, x
        y, lasty = lasty - q * y, y

    return (lastx, lasty, a)


def get_value(name, filetype):
    if filetype == 'bin':
        cipherlist = []
        for i in range(1, NUM):
            with open('{}'.format(i) + name, 'rb') as f:
                value = f.read()
                cipherlist.append(int.from_bytes(value, byteorder='big'))
        return cipherlist
    else:
        moduluslist = []
        for i in range(1, NUM):        
            with open('{}'.format(i) + name, 'r') as f:
                key = RSA.importKey(f.read())
                moduluslist.append(key.n)
        return moduluslist, key.e


if __name__ == '__main__':

    ciphertexts = get_value(CIPHER, 'bin')
    modulus, exp = get_value(MODULUS, 'rsa')

    C = chinese_remainder_theorem(ciphertexts, modulus)
    M = int(root(C, exp))
    M = M.to_bytes((M.bit_length() + 7)//8, byteorder='big')
    print(M)
