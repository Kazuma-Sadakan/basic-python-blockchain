from block import Block
from transaction import Transaction
from queue import PriorityQueue
from Crypto.Hash import SHA256
from copy import deepcopy
import json
from wallet import Wallet
from utils.constants import MINING_REWARD, DIFFICULTY


class Blockchain:
    def __init__(self):
        self.last_block = Block(tx_list = [], 
                                    previous_block_hash = "", 
                                    nonce = 0, 
                                    difficulty = DIFFICULTY, 
                                    index = 0, 
                                    timestamp = 0)
        
    def get_last_block_header(self):
        return self.last_block.header.to_dict()

    def add_block(self, block):
        block.previous_block = self.last_block
        self.last_block = block

    def get_utxos(self, address):
        current_block = self.last_block
        utxos = []
        while current_block.previous_block:
            for transaction in current_block.transactions:
                utxos.extend(transaction.get_outputs_by_address(address))
            current_block = current_block.previous_block
        return utxos
    
    def save(self):
        with open('blockchain.json', mode = 'w') as f:
            chain = []
            current_block = self
            while current_block:
                chain.append(current_block.to_dict())
                current_block = current_block.previous_block
            self.chain.reverse()
            f.write(json.dumps(self.chain))

    def load(self):
        with open('blockchain.json', mode = 'r') as f:
            blockchain = f.read()
            blockchain = json.loads(blockchain)
            self.last_block = None 
            for i, block in enumerate(blockchain):
                if i == 0:
                    continue 
                block = Block.load(block)
                block.previous_block = self.last_block
                self.last_block = block
