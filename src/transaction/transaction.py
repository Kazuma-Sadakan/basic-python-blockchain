import sys 
import os 
import json
import time 
import sys
import copy 
import hashlib

from .transaction_in import TransactionInput
from .transaction_out import TransactionOutput

from src.utils.utils import double_sha256
# sys.path.append(sys.path[0] + "/..")
# from wallet.wallet import Wallet

"""
{'tx_hash': 0, 
'vin': [
            {'tx_hash': 13, 
            'tx_output_n': 0, 
            'script_sig': '12345\t54321'}, 
            {'tx_hash': 12, 
            'tx_output_n': 1, 
            'script_sig': ''}
            ], 
'vout': [
            {'value': 100, 
                'script_pubkey': 'OP_DUP\tOP_HASH160\t123\tOP_EQUALVERIFY\tOP_CHECKSIG'}, 
            {'value': 200, 
                'script_pubkey': 'OP_DUP\tOP_HASH160\t234\tOP_EQUALVERIFY\tOP_CHECKSIG'}
            ]
}, 

"""


class Transaction:
    def __init__(self, vin, vout, version=0, time = 0):
        self.version = version
        self.locktime = time
        self.vin = vin
        self.vout = vout
        self.tx_hash = None

        self.tx_hash = self.__hash()

    def __hash(self):
        return double_sha256(self.to_json())

    def to_dict(self):
        return {
            "tx_hash": self.tx_hash,
            "version": self.version,
            "locktime": self.locktime,
            "vin": list(map(lambda tx_in: tx_in.to_dict() if tx_in is not None else None, self.vin)),
            "vout": [tx_out.to_dict() for tx_out in self.vout]
        }

    def to_json(self):
        return json.dumps(self.to_dict())



  