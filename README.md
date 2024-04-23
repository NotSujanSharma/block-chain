# Block Chain (From Scratch - Python)

To run the project you need to install requirements from requirement.txt

```
pip3 install -r requirements.txt
```

Genesis block is not created by default, you need to modify main.py to create genesis block, uncomment blockchain.create_genesis_block(), and comment connect_to_seeds(blockchain). The default port for first node is set to 8001 by default. You need to first run the project on port 8001 after modifying code.

```
python3 main.py 8001
```

After that you can run the project in any port you like (run unmodified project after first node is created)

```
python3 main.py 8000
```

By default communication feature is implemented (not completely). You can type anything and hit enter that will create a block in block chain, sign it with your private key and then broadcast the message to other peers.

Developed by Sujan Sharma
