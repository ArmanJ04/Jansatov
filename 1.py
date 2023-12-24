import random
import hashlib

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    max_div = int(n**0.5) + 1
    for d in range(3, max_div, 2):
        if n % d == 0:
            return False
    return True

def generate_prime_number():
    while True:
        num = random.randint(2, 100)
        if is_prime(num):
            return num

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_key_pair():
    prime1 = generate_prime_number()
    prime2 = generate_prime_number()
    n = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)
    e = 65537
    d = mod_inverse(e, phi)
    return ((n, e), (n, d))

def encrypt(message, public_key):
    n, e = public_key
    ciphertext = [pow(ord(char), e, n) for char in message]
    return ciphertext

def decrypt(ciphertext, private_key):
    n, d = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return decrypted_message

public_key, private_key = generate_key_pair()
message = "Hello, RSA!"

encrypted_message = encrypt(message, public_key)
decrypted_message = decrypt(encrypted_message, private_key)
print(f"Original Message: {message}")
print(f"Encrypted Message: {encrypted_message}")
print(f"Decrypted Message: {decrypted_message}")
