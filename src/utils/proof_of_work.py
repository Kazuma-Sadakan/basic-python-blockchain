import hashlib
import json

class ProofOfWork:
    def __init__(self):
        pass 
    
    @staticmethod
    def get_nonce(self, merkle_root, previous_block_hash, difficulty):
        nonce = 0
        block_hash = None 
        while not block_hash.startswith("0" * difficulty):
            nonce += 1
            data = {
                "merkle_root": merkle_root,
                "prev_block_hash": previous_block_hash,
                "nonce": nonce
            }
            block_hash = hashlib.sha256(json.dumps(data).encode("utf-8")).hexdigest()
        else:
            return nonce 

    # ---------- validation-------------
    @staticmethod
    def is_valid_proof(merkle_root, previous_block_hash, difficulty, nonce):
        data = {
            "merkle_root": merkle_root,
            "prev_block_hash": previous_block_hash,
            "nonce": nonce
        }
        block_hash = hashlib.sha256(json.dumps(data).encode("utf-8")).hexdigest()
        return block_hash.startswith("0"*difficulty)


    
