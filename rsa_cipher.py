import random
import math
from dataclasses import dataclass
from typing import Tuple

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            return False
    return True

def fpb(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e: int, phi: int) -> int:
    def extended_fpb(a, b):
        if a == 0:
            return b, 0, 1
        fpb, x1, y1 = extended_fpb(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return fpb, x, y
    fpb, x, y = extended_fpb(e, phi)
    return x % phi

def generate_rsa_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Kedua angka harus prima.")
    elif p == q:
        raise ValueError("nilai p dan q tidak boleh sama.")

    n = p * q

    phi = (p - 1) * (q - 1)

    e = 65537
    if fpb(e, phi) != 1:
        raise ValueError("e dan phi bukan prima.")
    
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def string_to_int(message: str) -> int:
    result = 0
    for char in message:
        result = result * 256 + ord(char)
    return result

def int_to_string(message_int: int) -> str:
    result = []
    while message_int > 0:
        result.append(chr(message_int % 256))
        message_int //= 256
    return ''.join(result[::-1])

def encrypt(public_key: Tuple[int, int], plaintext: str) -> list:
    e, n = public_key
    chunk_size = (n.bit_length() - 1) // 8
    chunks = [plaintext[i:i + chunk_size] for i in range(0, len(plaintext), chunk_size)]
    cipher_text = [pow(string_to_int(chunk), e, n) for chunk in chunks]
    return cipher_text

def decrypt(private_key: Tuple[int, int], cipher_text: list) -> str:
    d, n = private_key
    decrypted_chunks = [int_to_string(pow(chunk, d, n)) for chunk in cipher_text]
    return ''.join(decrypted_chunks)