import json
from typing import List

from .transaction_in import TransactionInput
from .transaction_out import TransactionOutput
from src.utils.utils import double_sha256
from src.block.utxo_pool import get_utxo
from src.block.memory_pool import tx_exists, tx_in_exists, tx_out_exists

class Transaction:
    def __init__(self, 
                vin:List[TransactionInput], 
                vout:List[TransactionOutput], 
                version:int, 
                locktime:float):

        self.vin = vin
        self.vout = vout
        self.version = version
        self.locktime = locktime

        self.tx_hash = None
        self.tx_hash = self._hash()

    def __hash__(self):
        return hash(self.tx_hash)

    def __eq__(self, other):
        return isinstance(other, Transaction) and self.to_dict() == other.to_dict()

    def _hash(self) -> str:
        return double_sha256(self.to_json())

    def get_tx_out(self, tx_output_n:int) -> TransactionOutput:
        if tx_output_n > len(self.vout) - 1:
            return -1
        return self.vout[tx_output_n]

    def valid_funds(self) -> bool:
        return self.total_vin_value() >= self.total_vout_value()

    @property 
    def total_vout_value(self) -> float:
        return sum([tx_out["value"] for tx_out in self.vout[:]])
    
    @property
    def total_vin_value(self, address) -> float:
        total_vin_value = 0
        for tx_in in self.vin[:]:
            total_vin_value += get_utxo(address = address, 
                                        tx_hash = tx_in.tx_hash, 
                                        tx_output_n = tx_in.tx_output_n)["value"]
        return total_vin_value

    @property
    def fees(self):
        return float(self.total_vin_value - self.total_vout_value)

    def in_mempool(self, address) -> bool:
        if tx_exists(tx_hash = self.tx_hash):
            return True 

        if any([tx_in_exists(address = address, 
                             tx_hash = tx_in["tx_hash"], 
                             tx_output_n = tx_in["tx_output_n"]) for tx_in in self.vin[:]]):
            return True 

        if any([tx_out_exists(tx_hash = tx_in["tx_hash"], 
                              tx_output_n = tx_in["tx_output_n"]) for tx_in in self.vin[:]]):
            return True 
        return False 

    @classmethod
    def load(cls, tx:dict):
        vin = [TransactionInput(**tx_in) for tx_in in tx["vin"]]
        vout = [TransactionOutput(**tx_out) for tx_out in tx["vout"]]
        return cls(vin = vin, vout = vout, version = tx["version"], time = tx["time"])

    def to_dict(self) -> dict:
        return {
            "tx_hash": self.tx_hash,
            "version": self.version,
            "locktime": self.locktime,
            "vin": [vars(tx_in) for tx_in in self.vin],
            "vout": [vars(tx_out) for tx_out in self.vout]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())



  