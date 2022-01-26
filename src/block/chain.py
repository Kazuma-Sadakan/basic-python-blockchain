import json
from copy import deepcopy

from .block import Block, BlockHead
from src.transaction.transaction import Transaction
from src.transaction.transaction_out import TransactionOutput
from src.utils.constants import DIFFICULTY
from src.utils.proof_of_work import ProofOfWork

block_head = BlockHead(version = 0, 
                    previous_block_hash = "", 
                    merkle_root_hash = "", 
                    timestamp = 0, 
                    difficulty = DIFFICULTY, 
                    nonce = 0)
genesis_block = Block(tx_list = [],
                    block_head = block_head)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.height = len(self.chain) - 1

    def get_block(self, block_height:int) -> Block:
        block = self.chain[block_height]
        head = BlockHead(**block["head"])
        tx_list = [Transaction.load(**tx) for tx in block["tx_list"]]
        block = Block(tx_list=tx_list, block_head=head)
        return block 

    @property
    def last_block(self):
        return self.get_block(self.height)

    def add_block(self, 
                block:dict):

        self.chain.append(block)
        self.height += 1

    def get_utxo(self, 
                block_height:int,
                tx_hash:str, 
                tx_output_n:int) -> TransactionOutput:

        block = self.get_block(block_height)
        tx = block.get_transaction(tx_hash)
        txout = tx.vout[tx_output_n]
        return txout
    
    def save(self):
        with open('blockchain.json', mode = 'w') as f:
            f.write(json.dumps(self.chain))

    def load(self):
        with open('blockchain.json', mode = 'r') as f:
            chain = f.read()
            self.chain = json.loads(chain)

    def length(self, other):
        return self.height >= other.height

    def __iter__(self):
        for i in range(self.height):
            yield i, self.get_block(i)

    def verify_chain(self):
        for i in range(1, self.height): 
            prev_block = self.get_block(i - 1)
            block = self.get_block(i)

            if block.head.prev_block_hash != prev_block.head.block_hash:
                return False 

            elif not block.verify_block():
                return False
        return True

