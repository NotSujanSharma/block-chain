from block import Block
from blockchain import Blockchain

def main():
    blockchain = Blockchain(4) 
    blockchain.add_block("Sujan Sent 1 BTC to Sharma")
    blockchain.add_block("Sharma Sent 2 BTC to Abcedi")
    blockchain.add_block("Abcedi Sent 3 BTC to 0x69")

    print("Blockchain:")
    for block in blockchain.chain:
        print(block)

    print(f"Is blockchain valid? {blockchain.is_valid()}")
if __name__ == "__main__":
    main()