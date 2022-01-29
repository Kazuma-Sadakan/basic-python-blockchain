import json
from copy import deepcopy

from .block import Block, BlockHead
from src.transaction.transaction import Transaction
from src.transaction.transaction_out import TransactionOutput
from src.utils.constants import DIFFICULTY
from src.utils.proof_of_work import ProofOfWork
from src.utils.utils import double_sha256

block_head = BlockHead(**{'_version': 0, 
                        '_previous_block_hash': "", 
                        '_merkle_root_hash': "", 
                        '_difficulty': 0, 
                        '_nonce': 0, 
                        '_timestamp': 0})

genesis_block = Block(**{'_tx_list': [],
                       '_block_head': block_head})

class Blockchain:
    def __init__(self):
        self.chain = [genesis_block]
        self.height = len(self.chain) - 1

    @property
    def last_block(self):
        return self[self.height]

    def __getitem__(self, _block_height:int) -> Block:
        return self.chain[_block_height]

    def get_tx(self, _block_height:int, _tx_hash:str) -> Transaction:
        tx = self[_block_height].get_transaction(_tx_hash)
        return tx

    def get_txo(self, 
                _block_height:int,
                _tx_hash:str, 
                _tx_output_n:int) -> TransactionOutput:

        tx = self.get_tx(_block_height, _tx_hash)
        tx_out = tx.vout[_tx_output_n]
        return tx_out 

    def add_block(self, _block:dict):
        self.chain.append(_block)
        self.height += 1
    
    def save(self):
        with open('blockchain.json', mode = 'w') as f:
            f.write(json.dumps(self.chain))

    def _load(self, _block:dict):
        block_head = BlockHead(**_block["head"])
        tx_list = [Transaction.load(**tx) for tx in _block["tx_list"]]
        block = Block(_tx_list = tx_list , _block_head = block_head)
        self.chain.append(block)
        

    def load(self):
        with open('blockchain.json', mode = 'r') as f:
            chain = f.read()
            chain = json.loads(chain)
            for block in chain:
                self._load(block)
            self.height = len(self.chain) - 1

    @staticmethod
    def verify_chain(self):
        for i in range(1, self.height): 
            prev_block = self.chain[i - 1]
            block = self.chain[i]
            if block.head.prev_block_hash != double_sha256(json.dumps(prev_block.head.to_json())):
                return False 

            pow_input = vars(block).copy().pop("version")
            if not ProofOfWork.valid_nonce(**pow_input):
                return False
        return True

    def copy(self, _chain:dict):
        for block in _chain:
            self._load(block)
        self.height = len(self.chain) - 1

    def items(self):
        for i, block in enumerate(self.chain):
            yield i, block

    def __iter__(self):
        for block in enumerate(self.chain):
            yield block


