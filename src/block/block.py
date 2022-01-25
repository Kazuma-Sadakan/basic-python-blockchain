import json
import os
import sys  
from time import time 
from copy import deepcopy

sys.path.append(sys.path[0] + "/..")
from transaction.transaction import Transaction
from utils.utils import MerkleTree
from utils.constants import DIFFICULTY
from Crypto.Hash import SHA256

"""
{'id': 0, 
'prev_block_hash': '452cbf687d85b5f0cd587be9bb157cf58fb43d97a3aeef255eecdad173d799a7', 
'merkle_root': '98a861ec4983e3562f38168b276e0edf63afcbb2503ace3a5a226c0de2048a4b', 
'nonce': 0, 'difficulty': 3, 
'timestamp': 1642936299.39131, 
'block_hash': '0a1bd5d6a31f8597b396f2d5ec5f782016fdca52b05befb27146a64c3470eabd', 
'tx_list': [
            {'id': 0, 
           'txin_list': [
                        {'last_tx_id': 13, 
                        'last_txout_idx': 0, 
                        'script_sig': '12345\t54321'}, 
                        {'last_tx_id': 12, 
                        'last_txout_idx': 1, 
                        'script_sig': ''}
                        ], 
           'txout_list': [
                        {'value': 100, 
                         'script_pubkey': 'OP_DUP\tOP_HASH160\t123\tOP_EQUALVERIFY\tOP_CHECKSIG'}, 
                        {'value': 200, 
                         'script_pubkey': 'OP_DUP\tOP_HASH160\t234\tOP_EQUALVERIFY\tOP_CHECKSIG'}
                        ]
            }, 
            {'id': 0, 
            'txin_list': [
                        {'last_tx_id': 13, 
                        'last_txout_idx': 0, 
                        'script_sig': '12345\t54321'}, 
                        {'last_tx_id': 12, 
                        'last_txout_idx': 1, 
                        'script_sig': ''}
                        ], 
            'txout_list': [
                        {'value': 100, 
                        'script_pubkey': 'OP_DUP\tOP_HASH160\t123\tOP_EQUALVERIFY\tOP_CHECKSIG'}, 
                        {'value': 200, 
                        'script_pubkey': 'OP_DUP\tOP_HASH160\t234\tOP_EQUALVERIFY\tOP_CHECKSIG'}
                        ]
            }
            ]
}
"""

class BlockHeader:
    def __init__(self, 
                previous_block_hash, 
                merkle_root, 
                nonce, 
                difficulty, 
                timestamp):

        self.prev_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.nonce = nonce
        self.difficulty = difficulty
        self.timestamp = timestamp
        self.block_hash = SHA256.new(self.to_json().encode("utf-8")).hexdigest()
            
    def __eq__(self, other):
        if self.__dict__ == other.to_dict():
            return True  
        return False 

    def to_dict(self):
        return deepcopy(self.__dict__)

    def to_json(self):
        return json.dumps(self.__dict__)


class Block: 
    def __init__(self, 
                tx_list, 
                previous_block_hash, 
                nonce, 
                difficulty, 
                previous_block = None,
                id = None, 
                timestamp = time()): 

        self.id = id
        self.header = BlockHeader(previous_block_hash = previous_block_hash,
                                merkle_root = self.get_merkle_root(tx_list),
                                nonce = nonce, 
                                difficulty = difficulty,
                                timestamp = timestamp)
        self.tx_list = tx_list
        self.previous_block = previous_block

    @staticmethod
    def verify_merkle_root(self, merkle_root, tx_list):
        assert MerkleTree.verify_merkle_root(merkle_root, tx_list)

    def get_transaction(self, tx_id):
        return filter(lambda tx: tx.id == tx_id, self.tx_list)

    def get_merkle_root(self, tx_list):
        return MerkleTree.generate_merkle_root([tx.to_dict() for tx in tx_list])

    def to_dict(self): 
        block = deepcopy(self.__dict__) 
        block.update({"tx_list" : [tx.to_dict() for tx in self.tx_list]}) 
        block.update({"header": self.header.to_dict()}) 
        block.pop("previous_block")
        return block 

    @staticmethod 
    def load(block): 
        block.update({"tx_list" : [Transaction(**transaction) for transaction in block["tx_list"]]})
        header = block.pop("header")
        return Block(**block, **header)


if __name__ == "__main__":
    tx = Transaction.load({"id": 0, "txin_list": [{"last_tx_id": 13, "last_txout_idx": 0, "script_sig": "12345\t54321"},\
         {"last_tx_id": 12, "last_txout_idx": 1, "script_sig": ""}], \
          "txout_list": [{"value": 100, "script_pubkey": "OP_DUP\tOP_HASH160\t123\tOP_EQUALVERIFY\tOP_CHECKSIG"}, \
         {"value": 200, "script_pubkey": "OP_DUP\tOP_HASH160\t234\tOP_EQUALVERIFY\tOP_CHECKSIG"}]})

    genesis_block = Block(tx_list = [],
                        previous_block_hash = "",
                        nonce = 0,
                        difficulty=DIFFICULTY,
                        id = 0,
                        timestamp = time())

    b1 = Block(tx_list = [tx, tx],
                previous_block_hash = genesis_block.header.block_hash,
                nonce = 0,
                difficulty = DIFFICULTY,
                id = 0,
                timestamp = time())

    print(b1.header.block_hash)
    print(b1.to_dict())