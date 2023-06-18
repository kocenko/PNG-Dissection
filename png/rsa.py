from math import gcd
from sympy import randprime
import random

BITS = 2048
BLOCK_SIZE = 64

def find_e(phi):
    while True:
        e = random.randint(2, phi)
        if gcd(e, phi) == 1:
            return e
        
def xgcd(a, m):
    t0, t1 = 0, 1
    r0, r1 = 1, 0
    while a != 0:
        (q, a), m = divmod(m, a), a
        t0, t1 = t1, t0 - q * t1
        r0, r1 = r1, r0 - q * r1
    return m, t0, r0

def modinv(a, m):
    g, t0, _ = xgcd(a, m)
    if g != 1:
        raise Exception('gcd(a, b) != 1')
    return t0 % m

def generate_rsa_keys():
    half_bits = BITS // 2

    min_p = (1 << half_bits)          # Min number of bit length: BITS // 2 + 1 
    max_p = (1 << half_bits + 1) - 1  # Max number of bit length: BITS // 2 + 1
    min_q = (1 << half_bits - 2)      # Min number of bit length: BITS // 2 - 1
    max_q = (1 << half_bits - 1) - 1  # Max number of bit length: BITS // 2 - 1

    p = randprime(min_p, max_p + 1)
    q = randprime(min_q, max_q + 1)

    n = p * q

    while n.bit_length() != BITS:
        p = randprime(min_p, max_p + 1)
        q = randprime(min_q, max_q + 1)
        n = p * q

    phi = (p - 1) * (q - 1)

    e = find_e(phi)
    d = modinv(e, phi)

    public_key = (e, n)
    private_key = (d, n)
    return private_key, public_key

def ecb_encrypt(bytes_str, public_key):
    e, n = public_key
    plaintext_int = int.from_bytes(bytes_str, byteorder="big")
    ciphertext = pow(plaintext_int, e, n)
    return ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, "big")  # Plus 7 is for rounding up

def ecb_decrypt(bytes_str, private_key):
    d, n = private_key
    ciphertext_int = int.from_bytes(bytes_str, byteorder="big")
    plaintext_bytes = pow(ciphertext_int, d, n)
    return plaintext_bytes.to_bytes((plaintext_bytes.bit_length() + 7) // 8, "big")  # Plus 7 is for rounding up)

if __name__ == '__main__':
    priv, pub = generate_rsa_keys()
    info = b'Hello World'
    cipher = ecb_encrypt(info, pub)
    plain = ecb_decrypt(cipher, priv)