import json
from copy import deepcopy


class TransactionInput:
    def __init__(self, last_tx_id, last_txout_idx, script_sig=None):
        self.last_tx_id = last_tx_id
        self.last_txout_idx = last_txout_idx
        self.script_sig = script_sig 

    def to_dict(self):
        return deepcopy(self.__dict__)

    def to_json(self):
        return json.dumps(self.__dict__)

    def set_script_sig(self, signature, pub_key):
        self.script_sig = f"{signature}\t{pub_key}"
        

if __name__ == "__main__":
    txin_1 = {"last_tx_id": 13, "last_txout_idx": 0}
    txin_2 = {"last_tx_id": 12, "last_txout_idx": 1}
    txin_1 = TransactionInput(**txin_1)
    txin_2 = TransactionInput(**txin_2)
    script_sig = {"signature": "12345", "pub_key": "54321"}
    txin_1.set_script_sig(**script_sig)
    print(txin_1.to_json())