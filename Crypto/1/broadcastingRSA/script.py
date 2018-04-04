# from Crypto.PublicKey import RSA
import gmpy2
import binascii
import io
gmpy2.get_context().precision = 4096
# import base64
from base64 import b64decode
from binascii import unhexlify
from Crypto.PublicKey import RSA
from functools import reduce
from gmpy2 import root

exp = 5

ct1 = "1.enc"
ct2 = "2.enc"
ct3 = "3.enc"
ct4 = "4.enc"
ct5 = "5.enc"

md1 = "1.pub.pem"
md2 = "2.pub.pem"
md3 = "3.pub.pem"
md4 = "4.pub.pem"
md5 = "5.pub.pem"


def get_value(filename, t):
	if t == 'bin':
		with open(filename, 'rb') as f:
			value = f.read()
		return int.from_bytes(value, byteorder='big')
	else: 
		with open(filename, 'r') as f:
			key = RSA.importKey(f.read())
		return key.n


def chinese_remainder(n, a):
	sum = 0
	prod = reduce(lambda a, b: a*b, n)
 
	for n_i, a_i in zip(n, a):
		p = prod // n_i
		sum += a_i * mul_inv(p, n_i) * p
	return sum % prod


def mul_inv(a, b):
	b0 = b
	x0, x1 = 0, 1
	if b == 1: return 1
	while a > 1:
		q = a // b
		a, b = b, a%b
		x0, x1 = x1 - q * x0, x0
	if x1 < 0: x1 += b0
	return x1

C1 = get_value(ct1, 'bin')
C2 = get_value(ct2, 'bin')
C3 = get_value(ct3, 'bin')
C4 = get_value(ct4, 'bin')
C5 = get_value(ct5, 'bin')

ciphertexts = [C1, C2, C3, C4, C5]

N1 = get_value(md1, 'b64')
N2 = get_value(md2, 'b64')
N3 = get_value(md3, 'b64')
N4 = get_value(md4, 'b64')
N5 = get_value(md5, 'b64')

modulus = [N1, N2, N3, N4, N5]

result = (chinese_remainder(modulus, ciphertexts))
M = int(root(result, exp))
print(M.bit_length())
print(M)
M = M.to_bytes((M.bit_length() + 7)//8, byteorder='big')
print(M)
