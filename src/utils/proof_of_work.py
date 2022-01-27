import hashlib
import json
from src.utils.utils import double_sha256
class ProofOfWork:
    def __init__(self):
        pass 
    
    @staticmethod
    def get_nonce(merkle_root_hash, previous_block_hash, difficulty, timestamp):
        nonce = 0
        block_hash = None 
        while not block_hash.startswith("0" * difficulty):
            nonce += 1
            data = {
                "merkle_root_hash": merkle_root_hash,
                "prev_block_hash": previous_block_hash,
                "timestamp": timestamp,
                "nonce": nonce
            }
            block_hash = double_sha256(data)
        else:
            return nonce 

    @staticmethod
    def valid_nonce(merkle_root_hash, previous_block_hash, difficulty, timestamp, nonce):
        data = {
            "merkle_root_hash": merkle_root_hash,
            "prev_block_hash": previous_block_hash,
            "timestamp": timestamp,
            "nonce": nonce
        }
        block_hash = double_sha256(data)
        return block_hash.startswith("0" * difficulty)


    
