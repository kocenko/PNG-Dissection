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


if __name__ == '__main__':
    # priv, pub = generate_rsa_keys()
    priv = b'D\x8c\xcc{\xc8\xe0x\x11Yd\xd7\xcd\x8f*B\x9d\xb0\xac\x00\x88\xbaM\xdf?\xf1\xb8\xe4\xeev\xfcSx\xed\x15\xb2\xf3\xec|\xb9\xf5\xf2\xe3\xbeU\x05s\xc4\xc2\x1b\xefJ\xb9\xf6K\x0b\x86\x01\x02\xda]&#d\xcdw\xc5X\x82\x030\\F\x8a\x84h\xc3"*\xb0\x0b\x8e\x96\x1d@\xa61\xcc\xa7\x03\xf8\x1d\x16\xb6]\x89\xce\xcc\x996h\x02`\xc7\xa7\x1b\xb4\x07\xd0\x03|\x15uu\rA^r\xe7\xff\r\xd1\x89)Y\x85\x1d\xfek7\xe5C!\xf1\x98\x9d\x12\x0c\x8dUwg\xe5j~*\xe9\xcf\x99>\x1e\xfa\x957\x0el\xb7l&\x0c}\xd6\xe54\xb8Q%\x95\x1c\xd13\xa2\x8a\x87E\xa3A\xb7`y\xdc\xb9\x14\x90#P\xc6\x07RE\xaa\xc0\x9fVe\x00\x8c\x89!\xce\x1dh\xf4\x16\x94P\x12\x97\x05\xa6\xe2\x07z"x\xde\xb5\x8a\x1e\xcer!\xa5\xad\xb5\xbb\xc3\x04w\xdf\xfb\x92\x93\x85S,\xf6\xb0\x03U\xeb\xc9\xe07e\xd9rG\x90\xc1E\x12\xb6\xbc\x91\xf1$'



# priv = (25312919201977285385692712343325408870297424496805291692806274821927843675699131347632187922187423412382369338156600981750191221139343872903960025574500812998271351568275388589133851836334385353255605706750601584004685589404951976384426895089711792305222958677469341363658418464750869181993737155038365826591214171597658767784681098461290646756763375487161402872270548482329408830520538411784946881127155153239004286235123435237236810324192024664302377383904963892911653149808788004062946127746394273631893830488635832178444162326563890801282190364859037632735190683157814234852900975843420942379825455613479198872995, 25363471141831591443060439182696795795625891226069387467147760973453846895344933819842635987988556309844401742337469039911694692644358372590555251842263604762945090229370155584146027239104414801754342030411315526427060339773062245951494657780781336588672373296611656664478973882486518075336411856013132227378334288879161176860121812863366767729558328706628927225991592631103255701117853654555540841286499355478244866168718443605231350924019256532040727196009586962649421140537650336626896083486094085853963961842600779164964930021648375440348229029087928399352570032987189294072844756814489157983011336839720873525549)
# pub = (12702218691033810726949600090597262337522874534556519667590425992964502496940002842493190561452687352707016534078769441017053212622988729537284335006813088344453044814174027039811549906717725683549567790873313696309036001966257208616612642052474877853095164083670584634122303055528981967419346700599538458528191317783003606123865946552102597308007045015646552263843665209422443278797421949471014944440598475244546723157880493163816701395580929299488519832829849807818788300266882665364500085637689956342214830258819511444223942090173901829985145802982247451493747140265753012125970152558135199687444484307459958385419, 25363471141831591443060439182696795795625891226069387467147760973453846895344933819842635987988556309844401742337469039911694692644358372590555251842263604762945090229370155584146027239104414801754342030411315526427060339773062245951494657780781336588672373296611656664478973882486518075336411856013132227378334288879161176860121812863366767729558328706628927225991592631103255701117853654555540841286499355478244866168718443605231350924019256532040727196009586962649421140537650336626896083486094085853963961842600779164964930021648375440348229029087928399352570032987189294072844756814489157983011336839720873525549)
# info = b'\x01\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
# cipher = ecb_encrypt(info, pub)
# print(cipher)
# print(ecb_decrypt(cipher, priv) == info)