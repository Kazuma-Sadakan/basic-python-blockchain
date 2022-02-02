import json
import base64
import binascii

class TransactionOutput:
    def __init__(self, 
                value:float, 
                address:str):

        self.value = value
        self.address = address
        public_key_hash = binascii.hexlify(base64.b64decode(address)).decode()
        self.script_pubkey = f"OP_DUP\tOP_HASH160\t{public_key_hash}\tOP_EQUALVERIFY\tOP_CHECKSIG"

    def to_dict(self):
        return {
            "value": self.value,
            "script_pubkey": self.script_pubkey
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def load(cls, tx_out:dict):
        address = list(filter(lambda x: not x.startswith("OP_"), tx_out["script_sig"]))[0]
        return cls(tx_out["value"], address = address)