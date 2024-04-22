from block import Block
from blockchain import Blockchain

def start():
    blockchain=Blockchain(4,8000)
    blockchain.create_genesis_block()
    while True:
        data = input("Enter the data to be added to the blockchain: ")
        blockchain.add_block(data)
        print("Blockchain:")
        print(f"Is blockchain valid? {blockchain.is_valid()}")

if __name__ == "__main__":
    start()