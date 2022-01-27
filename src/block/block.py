import json
import os
import sys  
import time
from copy import deepcopy

from typing import List
from src.transaction.transaction import Transaction
from src.utils.utils import MerkleTree
from src.utils.constants import DIFFICULTY
from src.utils.utils import double_sha256
from src.utils.proof_of_work import ProofOfWork

class BlockHead:
    def __init__(self, 
                version:int, 
                previous_block_hash:str, 
                merkle_root_hash:str, 
                difficulty:float,
                nonce:int,
                timestamp:float
                ):
        self.version = version
        self.prev_block_hash = previous_block_hash
        self.merkle_root_hash = merkle_root_hash
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce

            
    def __eq__(self, other):
        if self.__dict__ == other.to_dict():
            return True  
        return False 

    @property 
    def block_hash(self):
        return double_sha256(self.to_json())

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.__dict__)


class Block: 
    def __init__(self, 
                tx_list:List[Transaction], 
                block_head:BlockHead,
                ): 

        self.head = block_head
        self.tx_counter = len(tx_list)
        self.tx_list = tx_list

    def __eq__(self, 
               other:BlockHead) -> bool:

        return (self.head.to_json() == other.head.to_json() and 
                json.dumps(self.tx_list) == json.dumps(other.tx_list))

    def get_transaction(self, tx_hash:str) -> Transaction:

        return filter(lambda tx: tx.tx_hash == tx_hash, self.tx_list)

    def to_dict(self) -> dict: 
        block = deepcopy(self.__dict__) 
        block.update({"header": self.head.to_dict()}) 
        block.update({"tx_list" : [tx.to_dict() for tx in self.tx_list]}) 
        return block 

    def to_json(self) -> str:
        return json.dumps(self.to_dict())



 