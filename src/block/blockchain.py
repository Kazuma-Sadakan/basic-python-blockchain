import json
from typing import List

from .block import Block, BlockHead
from src.transaction.transaction import Transaction
from src.transaction.transaction_out import TransactionOutput
from src.utils.constants import DIFFICULTY
from src.utils.proof_of_work import ProofOfWork
from src.utils.utils import double_sha256

def create_genesis() -> Block:
    block_head = BlockHead(**{'version': 0, 
                            'previous_block_hash': "", 
                            'merkle_root_hash': "", 
                            'difficulty': 0, 
                            'nonce': 0, 
                            'timestamp': 0})

    genesis_block = Block.load({'tx_list': [],
                                'block_head': block_head}) 
    return genesis_block

class Blockchain:
    def __init__(self, chain:List[Block] = None):
        self.hash_conflicts = False
        self.chain = [create_genesis()] if chain is None else chain 
        self.height = len(self.chain) - 1 

    @property 
    def last_block(self): 
        return self[-1] 

    def __getitem__(self, block_height:int) -> Block:
        if block_height > self.height:
            return -1
        return self.chain[block_height]

    def get_tx(self, block_height:int, tx_hash:str) -> Transaction:
        tx = self[block_height].get_tx(tx_hash)
        return tx

    def get_tx_out(self, 
                block_height:int,
                tx_hash:str, 
                tx_output_n:int) -> TransactionOutput:

        tx = self.get_tx(block_height, tx_hash)
        tx_out = tx.vout[tx_output_n]
        return tx_out 

    def add_block(self, block:Block):
        self.chain.append(block)
        self.height += 1
    
    def save_to_db(self):
        with open('blockchain.json', mode = 'w') as f:
            f.write(json.dumps(self.chain))
        
    def load_from_db(self):
        with open('blockchain.json', mode = 'r') as f:
            chain = f.read()
            chain = json.loads(chain)
            self.chain = []
            for block in chain:
                self.chain.append(Block.load(block = block))
            self.height = len(self.chain) - 1

    def verify_chain(self):
        for i in range(1, len(self.chain)): 
            prev_block = self.chain[i - 1]
            block = self.chain[i]
            if block.head.prev_block_hash != double_sha256(json.dumps(prev_block.head.to_json())):
                return False 

            pow_input = vars(block).copy().pop("version")
            if not ProofOfWork.valid_nonce(**pow_input):
                return False
        return True

    @classmethod
    def load(cls, chain:List[dict]):
        chain = []
        for block in chain:
            chain.append(Block.load(block))
        return cls(chain = chain)

    def to_dict(self):
        chain = []
        for block in self.chain:
            chain.append(block.to_dict())
        return chain

    def to_json(self):
        return json.dumps(self.to_dict())

    def items(self):
        for i, block in enumerate(self.chain):
            yield i, block

    def __iter__(self):
        for block in enumerate(self.chain):
            yield block


