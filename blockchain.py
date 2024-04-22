from block import Block
import ecdsa 
class Blockchain:
    def __init__(self, difficulty):
        self.chain = []
        self.difficulty = difficulty
        self.private_key, self.public_key = self.generate_keys()
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("Genesis Block", "0" * 64, public_key=self.public_key)
        genesis_block.mine(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(data, previous_block.hash, public_key=self.public_key)
        new_block.mine(self.difficulty)
        new_block.signature = self.sign_block(new_block)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                return False

            if not current_block.hash.startswith("0" * self.difficulty):
                return False

            if not self.verify_signature(current_block):
                return False

        return True

    def generate_keys(self):
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key().to_string().hex()
        return private_key, public_key

    def sign_block(self, block):
        data_string = f"{block.data}{block.previous_hash}{block.nonce}{block.public_key}".encode()
        signature = self.private_key.sign(data_string)
        return signature.hex()

    def verify_signature(self, block):
        data_string = f"{block.data}{block.previous_hash}{block.nonce}{block.public_key}".encode()
        public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(block.public_key), curve=ecdsa.SECP256k1)
        try:
            public_key.verify(bytes.fromhex(block.signature), data_string)
            return True
        except ecdsa.BadSignatureError:
            return False