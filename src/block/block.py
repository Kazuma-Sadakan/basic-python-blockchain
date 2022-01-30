import json
from typing import List

from src.transaction.transaction import Transaction
from src.utils.utils import double_sha256


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

    @property 
    def block_hash(self) -> str:
        return double_sha256(self.to_json())

    def __hash__(self):
        return hash(self.block_hash)

    def __eq__(self, other):
        return isinstance(other, BlockHead) and self.__dict__ == vars(other)

    def to_json(self):
        return json.dumps(self.__dict__)


class Block: 
    def __init__(self, 
                tx_list:List[Transaction], 
                block_head:BlockHead,
                ): 

        self.block_head = block_head
        self.tx_counter = len(tx_list)
        self.tx_list = tx_list

    @property
    def block_hash(self):
        return self.block_head.block_hash

    def __hash__(self):
        return  hash(self.block_head)

    def __eq__(self, other) -> bool:
        return (isinstance(other, Block) and
               (self.block_head == other.block_head) and 
               self.tx_list == other.tx_list)

    def get_tx(self, tx_hash:str) -> Transaction:
        return list(filter(lambda tx: tx.tx_hash == tx_hash, self.tx_list))

    @classmethod
    def load(cls, block:dict):
        tx_list = [Transaction.load(tx) for tx in block["tx_list"]]
        block_head = BlockHead(**block["block_head"])
        return cls(tx_list = tx_list, block_head = block_head)

    def to_dict(self) -> dict: 
        return {
            "block_head": vars(self.block_head),
            "tx_list":[tx.to_dict() for tx in self.tx_list]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())



 