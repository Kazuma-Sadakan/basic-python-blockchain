import sys 
import os 
import json
import sys
from Crypto.Hash import SHA256

from .transaction_in import TransactionInput
from .transaction_out import TransactionOutput
sys.path.append(sys.path[0] + "/..")
from wallet.wallet import Wallet

class Transaction:
    def __init__(self, txin_list, txout_list, id = None):
        self.txin_list = txin_list
        self.txout_list = txout_list
        self.id = self.__generate_transaction_id() if id is None else id

    def get_txins_by_pubkey(self, pub_key):
        pub_hashed_key = Wallet.hash160(pub_key)
        return filter(lambda txin: txin.script_sig.split("\t")[1].strip() == pub_hashed_key, self.txin_list)

    def get_txouts_by_idx(self, idx):
        return self.txout_list[idx]

    def __generate_transaction_id(self):
        data = {
            "txin_list": [tx_in.to_dict() for tx_in in self.txin_list],
            "txout_list": [tx_out.to_dict() for tx_out in self.txout_list]
        }
        return SHA256.new(json.dumps(data))

    def sign_transaction(self):
        """
            signature includes 
            previous transaction id 
            previous transactiou output index 
            previous transaction public key script 
            this transaction public key script 
            total amount to send 
        """

        pass


    @staticmethod
    def load(transaction):
        transaction["txin_list"] = [TransactionInput(**txin) for txin in transaction["txin_list"]]
        transaction["txout_list"] = [TransactionOutput(**txout) for txout in transaction["txout_list"]]
        return Transaction(**transaction)

    # def get_total_in_value(self, utxos):
    #     tot_vin = 0
    #     for tx_in in self.inputs:
    #         id = tx_in["id"]

    # def get_total_out_value(self):
    #     tot_vout = 0
    #     for tx_out in self.outputs:
    #         tot_vout += tx_out['value']


    def to_dict(self):
        return {
            "id": self.id,
            "txin_list": [tx_in.to_dict() for tx_in in self.txin_list],
            "txout_list": [tx_out.to_dict() for tx_out in self.txout_list]
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return self.to_json()

    def __str__(self):
        return self.to_json()

if __name__ == "__main__":
    txin_1 = {"last_tx_id": 13, "last_txout_idx": 0}
    txin_2 = {"last_tx_id": 12, "last_txout_idx": 1}
    txin_1 = TransactionInput(**txin_1)
    txin_2 = TransactionInput(**txin_2)
    script_sig = {"signature": "12345", "pub_key": "54321"}
    txin_1.set_script_sig(**script_sig)

    txout_1 = TransactionOutput(100, "123")
    txout_2 = TransactionOutput(200, "234")
    # print(txout_1.to_json())

    tx_1 = Transaction([txin_1, txin_2], [txout_1, txout_2], 0)
    print(tx_1.to_json())