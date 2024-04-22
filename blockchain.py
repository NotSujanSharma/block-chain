from block import Block
import ecdsa 
import socket
import threading
import json
class Blockchain:
    def __init__(self, difficulty, port=8000):
        self.chain = []
        self.difficulty = difficulty
        self.private_key, self.public_key = self.generate_keys()
        self.nodes = set() 
        self.port=port
        #self.addr = (socket.gethostbyname(socket.gethostname()), port)
        self.addr='127.0.0.1'
        self.start_server(port)

    def create_genesis_block(self):
        genesis_block = Block("Genesis Block", "0" * 64, public_key=self.public_key)
        genesis_block.mine(self.difficulty)
        genesis_block.signature = self.sign_block(genesis_block)
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(data, previous_block.hash, public_key=self.public_key)
        new_block.mine(self.difficulty)
        new_block.signature = self.sign_block(new_block)
        self.chain.append(new_block)
        if(self.is_valid() & self.verify_signature(new_block)):
            self.broadcast_block(new_block)
        

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
        print("Public Key: ", public_key)
        print("Private Key: ", private_key.to_string().hex())
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
            print("[-] Bad Signature")
            return False
        
    def start_server(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.listen(5)
        print(f"[*] Listening on {socket.gethostbyname(socket.gethostname())}:{port}")

        thread = threading.Thread(target=self.handle_connections, args=(server_socket,))
        thread.start()

    def handle_connections(self, server_socket):
        while True:
            conn, addr = server_socket.accept()
            print(f"[+] Connected with {addr}")
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

    def handle_client(self, conn, addr):
        try:
            buffer = b''
            while True:
                data = conn.recv(9000)
                if not data:
                    break

                buffer += data 

                try:
                    if True:
                        message = json.loads(buffer.decode())
                        buffer = message 
                        if message['type'] == 'new_chain':
                            print(f"[*] Received new chain")
                            chain = message['chain']
                            self.chain = []
                            for block_data in chain:
                                block = Block(
                                    block_data['data'],
                                    block_data['previous_hash'],
                                    block_data['nonce'],
                                    block_data['hash'],
                                    block_data['public_key'],
                                    block_data['signature']
                                )
                                if  self.is_valid_block(block):
                                    self.chain.append(block)

                            print("[*] Updated chain")



                        elif message['type'] == 'new_block':
                            print("[*] Received new block")
                            block = Block(
                                message['data'],
                                message['previous_hash'],
                                message['nonce'],
                                message['hash'],
                                message['public_key'],
                                message['signature']
                            )
                            
                            if  self.is_valid_block(block):
                                self.chain.append(block)
                                print("[*] Added block to chain")
                                self.broadcast_block(block)

                        elif message['type'] == 'new_node':
                            new_node = (message['node'][0], message['node'][1])
                            self.nodes.add(new_node)
                            self.send_self_node(new_node)                            

                            self.broadcast_chain()

                        elif message['type'] == 'response_node':
                            response_node = (message['node'][0], message['node'][1])
                            self.nodes.add(response_node)

                except json.JSONDecodeError:
                    print("[-] JSONDecodeError")
                    pass
        except OSError as e:
            print(f"Error handling client connection: {e}")
        finally:
            conn.close()

    def send_self_node(self, node):
        response = {
            'type': 'response_node',
            'node': (self.addr, self.port)
        }
        response_json = json.dumps(response)
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.connect(node)
        print(f"[*] Sending self node to {node}")
        node_socket.send(response_json.encode())
        node_socket.close()

    def is_valid_block(self, block):
        if len(self.chain) != 0:
            
            previous_block = self.chain[-1]

            if block.previous_hash != previous_block.hash:
                return False

        if not block.previous_hash.startswith("0" * self.difficulty):
            return False

        if not self.verify_signature(block):
            return False

        return True

    def broadcast_block(self, block):
        block_data = {
            'type': 'new_block',
            'data': block.data,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'hash' : block.hash,
            'public_key': block.public_key,
            'signature': block.signature
        }
        block_json = json.dumps(block_data)

        for node in self.nodes:
            
            try:
                node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                node_socket.connect(node)  
                node_socket.send(block_json.encode())
                node_socket.close()
                print(f"Broadcasted block to {node}")
            except:
                self.nodes.remove(node)
                print(f"Failed to broadcast block to {node}")

    def broadcast_chain(self):
        chain_data = []
        for block in self.chain:
            block_data = {
                'data': block.data,
                'previous_hash': block.previous_hash,
                'nonce': block.nonce,
                'hash' : block.hash,
                'public_key': block.public_key,
                'signature': block.signature
            }
            chain_data.append(block_data)

        chain_json = json.dumps({'type': 'new_chain', 'chain': chain_data})

        nodes_copy = self.nodes.copy()

        for node in nodes_copy:
            try:
                node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                node_socket.connect(node)
                node_socket.send(chain_json.encode())
                node_socket.close()
                print(f"Broadcasted chain to {node}")
            except:
                self.nodes.remove(node)
                print(f"Failed to broadcast chain to {node}")

