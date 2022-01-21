import json
from copy import deepcopy
from re import T

class TransactionOutput:
    def __init__(self, value, public_hashed_key = None, script_pubkey = None):
        self.value = value
        if public_hashed_key is not None or script_pubkey is not None:
            self.script_pubkey = f"OP_DUP\tOP_HASH160\t{public_hashed_key}\tOP_EQUALVERIFY\tOP_CHECKSIG"\
                if script_pubkey is None else script_pubkey
            self.script_pubkey = script_pubkey
        else:
            raise ValueError('public_hashed_key or script_pubkey needs to be not None')
        
    def to_json(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return deepcopy(self.__dict__)

    def set_script_pubkey(self, public_hashed_key):
        self.script_pubkey = f"OP_DUP\tOP_HASH160\t{public_hashed_key}\tOP_EQUALVERIFY\tOP_CHECKSIG"

if __name__ == "__main__":
    txout_1 = TransactionOutput(100, "123")
    txout_2 = TransactionOutput(200, "234")
    print(txout_1.to_json())