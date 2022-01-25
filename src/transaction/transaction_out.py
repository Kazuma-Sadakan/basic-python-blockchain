import json
import base64
import binascii

"""
{"value": 100, 
"script_pubkey": {
    "hex": ,
    "address":, 
    }
}
"""

class TransactionOutput:
    def __init__(self, value, address):
        self.value = value
        self.address = address
        public_key_hash = binascii.hexlify(base64.b64decode(address)).decode()
        self.script_pubkey = f"OP_DUP\tOP_HASH160\t{public_key_hash}\tOP_EQUALVERIFY\tOP_CHECKSIG"
            
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "value": self.value,
            "script_pubkey": {
                "hex": self.script_pubkey,
                "address": self.address
            }
        }
    