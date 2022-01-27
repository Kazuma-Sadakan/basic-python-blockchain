import json
from copy import deepcopy

from .block import Block, BlockHead
from src.transaction.transaction import Transaction
from src.transaction.transaction_out import TransactionOutput
from src.utils.constants import DIFFICULTY
from src.utils.proof_of_work import ProofOfWork
from src.utils.utils import double_sha256

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
        self.chain = [genesis_block.to_dict()]
        self.height = len(self.chain) - 1

    @property
    def last_block(self):
        return self.get_block(self.height)

    def get_block(self, block_height:int) -> Block:
        block = self.chain[block_height]
        block_head = BlockHead(**block["head"])
        tx_list = [Transaction.load(**tx) for tx in block["tx_list"]]
        block = Block(tx_list = tx_list, block_head = block_head)
        return block 

    def get_tx(self, block_height:int, tx_hash:str) -> Transaction:
        block = self.get_block(block_height)
        tx = block.get_transaction(tx_hash)
        return tx

    def get_txo(self, 
                block_height:int,
                tx_hash:str, 
                tx_output_n:int) -> TransactionOutput:

        tx = self.get_tx(block_height, tx_hash)
        txout = tx.vout[tx_output_n]
        return txout 

    def add_block(self, block:dict):
        self.chain.append(block)
        self.height += 1
    
    def save(self):
        with open('blockchain.json', mode = 'w') as f:
            f.write(json.dumps(self.chain))

    def load(self):
        with open('blockchain.json', mode = 'r') as f:
            chain = f.read()
            self.chain = json.loads(chain)
            self.height = len(self.chain) - 1

    def verify_chain(self):
        for i in range(1, self.height): 
            prev_block = self.chain[i - 1]
            block = self.chain[i]
            if block["head"]["prev_block_hash"] != double_sha256(json.dumps(prev_block["head"])):
                return False 
            
            elif not ProofOfWork.valid_nonce(block["head"]["merkle_root_hash"],
                                            block["head"]["previous_block_hash"],
                                            block["head"]["difficulty"],
                                            block["head"]["timestamp"],
                                            block["head"]["nonce"]):
                return False
        return True

    def __iter__(self):
        for i, block in enumerate(self.chain):
            yield i, block


