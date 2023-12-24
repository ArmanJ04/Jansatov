import hashlib
import random
from datetime import datetime

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = datetime.now()
        self.signature = None

class Block:
    def __init__(self, transactions, previous_hash=''):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = datetime.now()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.timestamp) + str(self.transactions) + str(self.nonce) + self.previous_hash
        return hashlib.sha256(data.encode()).hexdigest()

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.root = self.build_tree()

    def build_tree(self):
        if not self.transactions:
            return None
        if len(self.transactions) == 1:
            return hashlib.sha256(str(self.transactions[0]).encode()).hexdigest()

        hashes = [hashlib.sha256(str(tx).encode()).hexdigest() for tx in self.transactions]
        while len(hashes) > 1:
            new_hashes = []
            for i in range(0, len(hashes), 2):
                if i + 1 < len(hashes):
                    concat_data = hashes[i] + hashes[i + 1]
                else:
                    concat_data = hashes[i] + hashes[i]
                new_hashes.append(hashlib.sha256(concat_data.encode()).hexdigest())
            hashes = new_hashes
        return hashes[0]

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.current_transactions = []

    def create_genesis_block(self):
        return Block(transactions=[])

    def add_transaction(self, transaction, sender_private_key, recipient_public_key):
        encrypted_message = encrypt(f"{transaction.sender}->{transaction.recipient}:{transaction.amount}", recipient_public_key)
        signature = sign_message(encrypted_message, sender_private_key)
        transaction.signature = signature
        self.current_transactions.append(transaction)

    def add_block(self, proof):
        previous_hash = self.chain[-1].hash
        block = Block(transactions=self.current_transactions, previous_hash=previous_hash)
        self.proof_of_work(block, proof)
        self.chain.append(block)
        self.current_transactions = []

    def proof_of_work(self, block, proof):
        while block.hash[:4] != "0000":
            block.nonce += 1
            block.hash = block.calculate_hash()

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
    return ''.join(map(str, ciphertext))

def decrypt(ciphertext, private_key):
    n, d = private_key
    decrypted_message = ''.join([chr(pow(int(char), d, n)) for char in ciphertext.split()])
    return decrypted_message

def sign_message(message, private_key):
    hashed_message = hashlib.sha256(message.encode()).hexdigest()
    signature = encrypt(hashed_message, private_key)
    return signature

public_key_alice, private_key_alice = generate_key_pair()
public_key_bob, private_key_bob = generate_key_pair()

blockchain = Blockchain()

transaction1 = Transaction(sender="Alice", recipient="Bob", amount=10)
blockchain.add_transaction(transaction1, private_key_alice, public_key_bob)

transaction2 = Transaction(sender="Bob", recipient="Charlie", amount=5)
blockchain.add_transaction(transaction2, private_key_bob, public_key_alice)

blockchain.add_block(proof=12345)

for block in blockchain.chain:
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Transactions: {[vars(tx) for tx in block.transactions]}")
    print("--------------")
