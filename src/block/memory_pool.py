import json
import os
import redis 

# BASE_DIR = ""
# FILE_PATH = os.path.join(BASE_DIR, ".json")

# class MemoryPool:
#     def __init__(self):
#         self.pool = []
    
#     def get(self):
#         return deepcopy(self.pool)

#     def save(self):
#         with open(FILE_PATH, mode = 'w') as f:
#             f.write(json.dumps([transaction.to_dict() for transaction in self.pool]))

#     def load(self):
#         with open(FILE_PATH, mode = 'r') as f:
#             pool = f.read()
#             self.pool = [Transaction(**transaction) for transaction in json.loads(pool)]

#     def add_transaction(self, transaction):
#         self.pool.append(transaction)
#         self.save()


class Mempool:
    def __init__(self, _host, _port):
        self.redis = redis.Redis(host = _host, port = _port)
        
    def add_tx(self, transaction_hash, transaction):
        try:
            self.redis.set(transaction_hash, transaction)
            return True 
        except Exception as e:
            print(f"Error: {e}")
            return False 

    def get(self, transaction_hash):
        data = self.redis.get(transaction_hash)
        if data is None:
            return -1
        else:
            return data.decode()

    def get_all(self):
        for val in self.values:
            yield val.decode()

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

    @property
    def values(self):
        for key in self.redis.scan_iter():
            yield self.redis.get(key)

    @property
    def items(self):
        for key in self.redis.scan_iter():
            yield key.decode(), self.redis.get(key).decode()

    def __iter__(self):
        for key in self.redis.scan_iter():
            yield key.decode()

