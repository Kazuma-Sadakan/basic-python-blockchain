from re import M
import unittest
from src.transaction.transaction import Transaction 
from src.utils.proof_of_work import ProofOfWork
from src.utils.utils import MerkleTree
from src.block.block import Block, BlockHead
from src.block.memory_pool import get_all

class TestBlock(unittest.TestCase):
    def setUp(self):
        tx_list = get_all()
        tx_hash_list = [tx["tx_hash"] for tx in tx_list]
            
        merkle_root_hash = MerkleTree.generate_merkle_root(tx_hash_list)
        self.blockhead = BlockHead(version = 0, 
                              previous_block_hash = "123", 
                              merkle_root_hash = merkle_root_hash,
                              difficulty=3,
                              nonce=0,
                              timestamp=0
                              )
        tx_list = [Transaction.load(tx) for tx in tx_list]
        self.block = Block(tx_list = tx_list, block_head = self.blockhead)

    def test_blockhead_create(self):
        print(self.blockhead.to_json())

    def test_block_create(self):
        print(self.block.to_json())