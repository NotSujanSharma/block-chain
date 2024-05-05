# Block Chain (From Scratch - Python)

To run the project you need to install requirements from requirement.txt

```
pip3 install -r requirements.txt
```

## Usage:

Use port as your first argument.
You need to first create genesis block and run first node to establish connection. To create Genesis block use 8001 as your first argument and 'genesis' as your second argument.

```
python3 main.py 8001 genesis
```

If first node is already running on port 8001 and genesis block is created, use the port of your choice as first argument, do not enter anything as second argument.

```
python3 main.py 8000
```

By default communication feature is implemented (not completely). You can type anything and hit enter that will create a block in block chain, sign it with your private key and then broadcast the message to other peers.

Developed by Sujan Sharma
