import hashlib
import time
import ecdsa  # Install ecdsa library: pip install ecdsa

class Block:
    def __init__(self, data, previous_hash, nonce=0, public_key=None, signature=None):
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.public_key = public_key
        self.signature = signature
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_string = f"{self.data}{self.previous_hash}{self.nonce}{self.public_key}{self.signature}".encode()
        return hashlib.sha256(data_string).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                break
            self.nonce += 1

    def __str__(self):
        return f"Block(data: {self.data}, previous_hash: {self.previous_hash}, hash: {self.hash}, nonce: {self.nonce}, public_key: {self.public_key}, signature: {self.signature})"
