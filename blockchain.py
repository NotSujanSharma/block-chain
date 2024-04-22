from block import Block
class Blockchain:
    def __init__(self, difficulty):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("Genesis Block", "0" * 64)
        genesis_block.mine(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(data, previous_block.hash)
        new_block.mine(self.difficulty)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                return False

            if not current_block.hash.startswith("0" * self.difficulty):
                return False

        return True

