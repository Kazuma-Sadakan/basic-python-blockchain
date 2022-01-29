import json
from typing import List

from .transaction_in import TransactionInput
from .transaction_out import TransactionOutput
from src.utils.utils import double_sha256
from src.block.utxo_pool import UtxoDB

utxo_db = UtxoDB('localhost', 27017)
utxo_db.connect_db("utxo")
utxo_db.connect_collection("utxo")

class Transaction:
    def __init__(self, 
                _vin:List[TransactionInput], 
                _vout:List[TransactionOutput], 
                _version:int, 
                _locktime:float):

        self.vin = _vin
        self.vout = _vout
        self.version = _version
        self.locktime = _locktime

        self.tx_hash = None
        self.tx_hash = self._hash()

    def __hash__(self):
        return hash(self.tx_hash)

    def __eq__(self, other):
        return isinstance(other, Transaction) and self.to_dict() == other.to_dict()

    def _hash(self) -> str:
        return double_sha256(self.to_json())

    def get_tx_out(self, _tx_output_n:int) -> TransactionOutput:
        return self.vout[_tx_output_n]

    def get_total_vout_value(self) -> float:
        return sum([tx_out["value"] for tx_out in self.vout[:]])

    def valid_funds(self, _total_vin_value) -> bool:
        return _total_vin_value >= self.get_total_vout_value()

    def get_total_vin_value(self):
        total_vin_value = 0
        for tx_in in self.vin:
            total_vin_value += utxo_db.find_utxo(_address = _address, 
                                                _tx_hash = tx_in.tx_hash, 
                                                _tx_output_n = tx_in.tx_output_n)["value"]
        return total_vin_value

    @staticmethod
    def load(_tx:dict):
        vin = [TransactionInput(**tx_in) for tx_in in _tx["vin"]]
        vout = [TransactionOutput(**tx_out) for tx_out in _tx["vout"]]
        return Transaction(_vin = vin, _vout = vout, _version = _tx["version"], _time = _tx["time"])

    def to_dict(self) -> dict:
        return {
            "tx_hash": self.tx_hash,
            "version": self.version,
            "locktime": self.locktime,
            "vin": [vars(tx_in) for tx_in in self.vin],
            "vout": [vars(tx_out) for tx_out in self.vout]
        }

    def to_json(self) -> json:
        return json.dumps(self.to_dict())



  