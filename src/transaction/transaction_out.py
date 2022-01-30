import json
import base64
import binascii

class TransactionOutput:
    def __init__(self, 
                value:float, 
                address:str):

        self.value = value
        public_key_hash = binascii.hexlify(base64.b64decode(address)).decode()
        self.script_pubkey = f"OP_DUP\tOP_HASH160\t{public_key_hash}\tOP_EQUALVERIFY\tOP_CHECKSIG"
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__)
    