import json

"""
TransactionInput.to_json()

{"tx_hash": 13, 
"tx_output_n": 0, 
"script_sig": "<signature>\t<public_key>"  
}

"""

class TransactionInput:
    def __init__(self, 
                tx_hash:str, 
                tx_output_n:int,
                script_sig:str=""):

        self.tx_hash = tx_hash
        self.tx_output_n = tx_output_n
        self.script_sig = script_sig

    def to_dict(self) -> dict:
        return {
            "tx_hash": self.tx_hash,
            "tx_output_n": self.tx_output_n,
            "script_sig": self.script_sig,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

