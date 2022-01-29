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
    def __init__(self, 
                _value:float, 
                _address:str):

        self.value = _value
        public_key_hash = binascii.hexlify(base64.b64decode(_address)).decode()
        self.script_pubkey = f"OP_DUP\tOP_HASH160\t{public_key_hash}\tOP_EQUALVERIFY\tOP_CHECKSIG"
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__)
    