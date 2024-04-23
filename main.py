from block import Block
import sys
import asyncio
from blockchain import Blockchain

def start():
    port=int(sys.argv[1])
    blockchain=Blockchain(4,port)
    #blockchain.create_genesis_block()
    connect_to_seeds(blockchain)
    while True:
        data = input("Enter the data to be added to the blockchain: ")
        blockchain.add_block(data)
        print("Blockchain:")
        print(f"Is blockchain valid? {blockchain.is_valid()}")

def connect_to_seeds(blockchain):
    seed_nodes = [
        ('127.0.0.1', 8001),
    ]
    for node in seed_nodes:
        asyncio.run(blockchain.connect_node(node, new_node=True) )


if __name__ == "__main__":
    start()