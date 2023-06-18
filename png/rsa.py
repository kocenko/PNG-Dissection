from math import gcd
import libnum
import random

BITS = 1024
BLOCK_SIZE = 64

def ecb_encrypt(bytes_str, public_key):
    e, n = public_key
    plaintext_int = int.from_bytes(bytes_str, byteorder="big")
    ciphertext = pow(plaintext_int, e, n)
    return ciphertext.to_bytes(BITS // 8, "big")


def ecb_decrypt(bytes_str, private_key):
    d, n = private_key
    ciphertext_int = int.from_bytes(bytes_str, byteorder="big")
    plaintext_bytes = pow(ciphertext_int, d, n)
    # print(math.log2(plaintext_bytes))
    return plaintext_bytes.to_bytes(BLOCK_SIZE, "big")








def generate_rsa_key_pair():
    n = 0
    while n.bit_length() != BITS:
        p = libnum.generate_prime(BITS // 2 + 1)
        q = libnum.generate_prime(BITS // 2 - 1)

        n = p * q

    print(f"Key length: {n.bit_length()}")

    phi_n = (p - 1) * (q - 1)

    e = choose_public_exponent(phi_n)

    d = modular_inverse(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)
    return private_key, public_key


def choose_public_exponent(phi_n):
    while True:
        e = random.randint(2, phi_n)
        if gcd(e, phi_n) == 1:
            return e


def modular_inverse(a, m):
    t1, t2 = 0, 1
    r1, r2 = m, a
    while r2 != 0:
        quotient = r1 // r2
        t1, t2 = t2, t1 - quotient * t2
        r1, r2 = r2, r1 - quotient * r2
    if r1 > 1:
        raise ValueError("a is not invertible")
    if t1 < 0:
        t1 += m
    return t1