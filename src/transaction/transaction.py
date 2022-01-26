import sys 
import os 
import json
import time 
import sys
import copy 
import hashlib
from typing import List
from .transaction_in import TransactionInput
from .transaction_out import TransactionOutput

from src.utils.utils import double_sha256

class Transaction:
    def __init__(self, 
                _vin:List[TransactionInput], 
                _vout:List[TransactionOutput], 
                _version:int=0, 
                _locktime:float= 0):

        self.vin = _vin
        self.vout = _vout
        self.version = _version
        self.locktime = _locktime

        self.tx_hash = None
        self.tx_hash = self.__hash()

    def __hash(self) -> str:
        return double_sha256(self.to_json())

    @staticmethod
    def load(tx:dict):
        vin = [TransactionInput(**txin) for txin in tx["vin"]]
        vout = [TransactionOutput(**txout) for txout in tx["vout"]]
        version = tx["version"]
        return Transaction(_vin = vin, _vout = vout, _version = version, _time = tx["time"])

    def to_dict(self) -> dict:
        return {
            "tx_hash": self.tx_hash,
            "version": self.version,
            "locktime": self.locktime,
            "vin": list(map(lambda tx_in: tx_in.to_dict() if tx_in is not None else None, self.vin)),
            "vout": [tx_out.to_dict() for tx_out in self.vout]
        }

    def to_json(self) -> json:
        return json.dumps(self.to_dict())



  