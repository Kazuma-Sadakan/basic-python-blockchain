import json
import os
from itsdangerous import exc
import redis 

class Mempool:
    def __init__(self, _host, _port, _db = 0):
        try:
            self.redis = redis.Redis(host = _host, port = _port, db = _db)
        except Exception as e:
            print(e)

    def add_tx(self, _transaction_hash:str, _transaction:str):
        if isinstance(_transaction, dict):
            _transaction = json.dumps(_transaction)
        try:
            self.redis.set(_transaction_hash, _transaction)
            return _transaction 
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_tx(self, _transaction_hash:str):
        try:
            data = self.redis.get(_transaction_hash)
        except Exception as e:
            print(e)
        if data is None:
            return -1
        else:
            return data.decode()

    def get_all(self):
        tx_list = []
        for val in self.values:
            tx_list.append(val.decode())
        return  tx_list

    def remove(self, key):
        self.redis.delete(key)

    def remove_all(self):
        for key in self:
            self.remove(key)

    def get_keys(self):
        for key in self.redis.scan_iter():
            yield key.decode() 

    def find_one_in_vin(self, tx_hash, tx_output_n):
        for item in self.values:
            vin = json.loads(item)["vin"]
            for txin in vin:
                if txin["tx_hash"] == tx_hash and txin["tx_output_n"] == tx_output_n:
                    return True 
        else:
            return False 

    def find_one_in_vout(self, tx_hash, tx_output_n):
        try:
            data = json.loads(self.get(tx_hash))["vout"][tx_output_n]
            return data
        except Exception as e:
            print("Error: {e}")
            return False 

    def values(self):
        data_list = []
        for key in self.redis.scan_iter():
            data_list.append(self.redis.get(key))
        return data_list

    def items(self):
        data_list = []
        for key in self.redis.scan_iter():
            data_list.append([key.decode(), self.redis.get(key).decode()])
        return data_list

    def __iter__(self):
        for key in self.redis.scan_iter():
            yield key.decode()



mempool = Mempool("localhost", 6379)
mempool.add_tx("123", json.dumps({"name": "kazuma"}))
print(mempool.get_tx("12"))

redis = redis.Redis("localhost", 6379)
print(redis.exists("123"))