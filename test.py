import socket
import json

node_data = {
    'type': 'new_node',
    'node': ('127.0.0.1', 8001)
}

block_json = json.dumps(node_data)

node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
node_socket.connect(('127.0.0.1', 8000)) 
print(block_json.encode())
print(block_json.encode().decode())  
node_socket.send(block_json.encode())

node_socket.close()