import hashlib
import binascii
import json

from src.transaction.transaction_in import TransactionInput
from src.wallet.wallet import Wallet  

def double_sha256(data):
    encoded_data = json.dumps(data).encode()
    hashed_data = hashlib.sha256(encoded_data).digest()
    return hashlib.sha256(hashed_data).hexdigest()


def create_script_sig(signature, public_key):
    return "{}\t{}".format(signature, public_key)

def create_transaction_input(private_key, public_key, previous_transaction=None, tx_hash="", tx_output_n=0):
    signature = Wallet.generate_signature(private_key, previous_transaction, public_key)
    script_sig = create_script_sig(signature, public_key)
    return TransactionInput(tx_hash, tx_output_n, script_sig)



class MerkleTree:
    def __init__(self):
        pass
    
    def hash(node):
        return hashlib.sha256(binascii.hexlify(str(node).encode("utf-8"))).hexdigest()

    @staticmethod
    def generate_merkle_root(nodes):
        nodes = MerkleTree.hash(nodes)
        def recursive(nodes):
            tree = []
            if len(nodes) % 2 != 0:
                nodes.append(nodes[-1])
            temp = []
            for node in nodes:
                temp.append(node)
                if len(temp) % 2 == 0:
                    tree.append(MerkleTree.hash(temp[0]+temp[1]))
                    temp = []
            if len(tree) == 1:
                return tree[0]
            else:
                return recursive(tree)
        return recursive(nodes)

    @staticmethod
    def verify_merkle_root(merkle_root, nodes):
        return merkle_root == MerkleTree.generate_merkle_root(nodes)

if __name__ == "__main__":
    data = [1,2,3,4,5]
    merkle_root = MerkleTree.generate_merkle_root(data)
    print(merkle_root)
    print(MerkleTree.verify_merkle_root(merkle_root, data))
