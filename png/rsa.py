from math import gcd
from sympy import randprime
import random

BITS = 1024
BLOCK_SIZE = 64
NONCE = int.from_bytes(((56854645).to_bytes(BITS // 8, "big")), byteorder="big")

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

def bytes_padding(bytes_str):
    padding_length = 1 + (BLOCK_SIZE - len(bytes_str))
    padding = bytes([padding_length]) * padding_length   # To store information about padding
    return bytes_str + padding

def bytes_unpadding(bytes_str):
    padding_length = bytes_str[-1]
    return bytes_str[:-padding_length]

def ecb_encrypt(bytes_str, public_key):
    bytes_str = bytes_padding(bytes_str)
    e, n = public_key
    plaintext_int = int.from_bytes(bytes_str, byteorder="big")
    ciphertext = pow(plaintext_int, e, n)
    bytes_to_return = ciphertext.to_bytes(BITS // 8, "big")

    return bytes_to_return

def ecb_decrypt(bytes_str, private_key):
    d, n = private_key
    ciphertext_int = int.from_bytes(bytes_str, byteorder="big")
    plaintext_bytes = pow(ciphertext_int, d, n)
    bytes_to_return = plaintext_bytes.to_bytes(BLOCK_SIZE + 1, "big")
    bytes_to_return = bytes_unpadding(bytes_to_return)

    return bytes_to_return

def ctr_encrypt(bytes_str, public_key, counter):
    e, n = public_key
    plaintext_int = int.from_bytes(bytes_str, byteorder="big")
    a = counter + NONCE
    ciphertext = pow(a, e, n)
    msg = ciphertext ^ plaintext_int
    return msg.to_bytes(BITS // 8, "big")

def ctr_decrypt(bytes_str, private_key, counter):
    d, n = private_key
    ciphertext_int = int.from_bytes(bytes_str, byteorder="big")
    a = counter + NONCE
    plaintext_bytes = pow(a, d, n)
    msg = plaintext_bytes ^ ciphertext_int
    return msg.to_bytes(BITS // 8, "big")
