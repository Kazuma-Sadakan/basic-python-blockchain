import hashlib
import json

class ProofOfWork:
    def __init__(self):
        pass 
    
    @staticmethod
    def get_nonce(self, merkle_root_hash, previous_block_hash, difficulty, timestamp):
        nonce = 0
        block_hash = None 
        while not block_hash.startswith("0" * difficulty):
            nonce += 1
            data = {
                "merkle_root_hash": merkle_root_hash,
                "prev_block_hash": previous_block_hash,
                "nonce": nonce,
                "timestamp": timestamp
            }
            block_hash = hashlib.sha256(json.dumps(data).encode("utf-8")).hexdigest()
        else:
            return nonce 

    @staticmethod
    def valid_nonce(merkle_root_hash, previous_block_hash, difficulty, nonce, timestamp):
        data = {
            "merkle_root_hash": merkle_root_hash,
            "prev_block_hash": previous_block_hash,
            "nonce": nonce,
            "timestamp": timestamp
        }
        block_hash = hashlib.sha256(json.dumps(data).encode("utf-8")).hexdigest()
        return block_hash.startswith("0"*difficulty)


    
