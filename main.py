from block import Block
import asyncio
from blockchain import Blockchain

def start():
    blockchain=Blockchain(4,8000)
    blockchain.create_genesis_block()
    connect_to_seeds(blockchain)
    while True:
        data = input("Enter the data to be added to the blockchain: ")
        blockchain.add_block(data)
        print("Blockchain:")
        print(f"Is blockchain valid? {blockchain.is_valid()}")

def connect_to_seeds(blockchain):
    seed_nodes = [
        ('127.0.0.1', 8001),
        ('127.0.0.1', 8002),
        ('127.0.0.1', 8003)
    ]
    for node in seed_nodes:
        asyncio.run(blockchain.connect_node(node))


if __name__ == "__main__":
    start()