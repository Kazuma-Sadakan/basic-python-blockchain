import json

from typing import List
from src.transaction.transaction import Transaction
from src.utils.utils import double_sha256
from src.utils.proof_of_work import ProofOfWork

class BlockHead:
    def __init__(self, 
                _version:int, 
                _previous_block_hash:str, 
                _merkle_root_hash:str, 
                _difficulty:float,
                _nonce:int,
                _timestamp:float
                ):
        self.version = _version
        self.prev_block_hash = _previous_block_hash
        self.merkle_root_hash = _merkle_root_hash
        self.timestamp = _timestamp
        self.difficulty = _difficulty
        self.nonce = _nonce

    @property 
    def block_hash(self):
        return double_sha256(self.to_json())

    def __hash__(self):
        return hash(self.block_hash)

    def __eq__(self, other):
        return isinstance(other, BlockHead) and self.__dict__ == vars(other)

    def to_json(self):
        return json.dumps(self.__dict__)


class Block: 
    def __init__(self, 
                _tx_list:List[Transaction], 
                _block_head:BlockHead,
                ): 

        self.block_head = _block_head
        self.tx_counter = len(_tx_list)
        self.tx_list = _tx_list

    def __hash__(self):
        return  hash(self.block_head)

    def __eq__(self, other) -> bool:
        return (isinstance(other, Block) and
               (self.block_head == other.block_head) and 
               self.tx_list == other.tx_list)

    def get_transaction(self, tx_hash:str) -> Transaction:
        return filter(lambda tx: tx.tx_hash == tx_hash, self.tx_list)

    @staticmethod
    def load(_block:dict):
        tx_list = [Transaction.load(tx) for tx in _block["tx_list"]]
        block_head = BlockHead(**_block["block_head"])
        return Block(_tx_list = tx_list, _block_head = block_head)

    def to_dict(self) -> dict: 
        return {
            "block_head": vars(self.head),
            "tx_list":[tx.to_dict() for tx in self.tx_list]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())



 