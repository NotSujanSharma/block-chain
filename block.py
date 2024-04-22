import hashlib
import time

class Block:
    def __init__(self, data, previous_hash, nonce=0):
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_string = f"{self.data}{self.previous_hash}{self.nonce}".encode()
        return hashlib.sha256(data_string).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                break
            self.nonce += 1

    def __str__(self):
        return f"Block(data: {self.data}, previous_hash: {self.previous_hash}, hash: {self.hash}, nonce: {self.nonce})"

