import json
import redis 
from utxo_pool import get_utxo


HOST = "localhost"
PORT = 6379
DB = 0

mempool = redis.Redis(host = HOST, 
                      port = PORT, 
                      db = DB,
                      charset = "utf-8", 
                      decode_responses = True)

def add_tx(_tx_hash:str, _transaction:str) -> bool:
    try:
        if mempool.exists(_tx_hash):
            return False 
        success = mempool.set(_tx_hash, _transaction)
    except Exception as e:
        print(f"Error: {e}")
        return False
    return success

def get_tx(_tx_hash:str) -> int or str:
    try:
        data = mempool.get(_tx_hash)
    except Exception as e:
        print(f"Error: {e}")
        return -1
    if data is None:
        return -1
    else:
        return data

def get_all() -> int or list:
    tx_list = []
    for tx_hash in mempool.keys():
        try:
            tx = get_tx(_tx_hash = tx_hash)
            if tx == -1:
                raise ValueError("Transaction not found.")
        except Exception as e:
            print(f"Error: {e}")
            return -1
        tx_list.append(json.loads(tx))
    return tx_list
    
def delete(_tx_hash:str) -> bool:
        try:
            success = mempool.delete(_tx_hash)
        except Exception as e:
            print(e)
            return False
        return success

def delete_all() -> bool:
    for tx_hash in mempool.keys():
        success = delete(_tx_hash = tx_hash)
        if not success:
            return False 
    return True

def get_keys():
    for key in mempool.keys():
        yield key 

def tx_exists(_tx_hash:str) -> bool:
    try:
        exist = mempool.exists(_tx_hash)
    except Exception as e:
        print(e)
        return False 
    return exist

def tx_out_exists(_tx_hash:str, _tx_output_n:int) -> bool:
    transaction = get_tx(_tx_hash = _tx_hash)
    if transaction == -1:
        return -1
    tx = json.loads(transaction)
    vout = tx["vout"]
    try:
        tx_out = vout[_tx_output_n]
    except IndexError as e:
        print(e)
        return False 
    if tx_out is None:
        return False
    return True

def tx_in_exists(_address, _tx_hash, _tx_output_n) -> bool:
    try:
        transaction = get_utxo(_address = _address, 
                                _tx_hash = _tx_hash, 
                                _tx_output_n = _tx_output_n)
        tx = get_tx(_tx_hash = transaction["tx_hash"])
        tx = json.loads(tx)
        vin = tx["vin"]
        return True
    except Exception as e:
        print("Error: {e}")
        return False 


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


# class Mempool:
#     def __init__(self, _host, _port, _db = 0):
#         self.redis = redis.Redis(host = _host, port = _port, db = _db)
        
#     def add_tx(self, _transaction_hash, _transaction):
#         try:
#             self.redis.set(_transaction_hash, _transaction)
#             return True 
#         except Exception as e:
#             print(f"Error: {e}")
#             return False 

#     def get_tx(self, _tx_hash):
#         try:
#             data = self.redis.get(_tx_hash)
#         except Exception as e:
#             print(f"Error: {e}")
#             return -1
#         if data is None:
#             return -1
#         else:
#             return data.decode()

#     def get_all(self):
#         try:
#             data =  [val.decode() for val in self.values]
#         except Exception as e:
#             print(e)
#             return -1
#         return data
        

#     def delete(self, _key):
#         if self.redis.exists(_key) == 1:
#             try:
#                 self.redis.delete(_key)
#             except Exception as e:
#                 print(e)
#                 return False
#             return True
#         else:
#             return False 

#     def delete_all(self):
#         for key in self:
#             self.delete(key)

#     def get_keys(self):
#         for key in self.redis.scan_iter():
#             yield key.decode() 

#     def tx_exists(self, _tx_hash) -> bool:
#         exist = self.get_tx(_tx_hash = _tx_hash)
#         return exist

#     def tx_out_exists(self, _tx_hash, _tx_output_n) -> bool:
#         transaction = self.get_tx(_tx_hash = _tx_hash)
#         tx = json.loads(transaction)
#         vout = tx["vout"]
#         for tx_in in vout:
#             if tx_in["tx_output_n"] == _tx_output_n:
#                 return True 
#         else:
#             return False 

#     def tx_in_exists(self, _address, _tx_hash, _tx_output_n) -> bool:
#         try:
#             transaction = utxo_db.find_utxo(_address = _address, 
#                                             _tx_hash = _tx_hash, 
#                                             _tx_output_n = _tx_output_n)
#             tx = self.get_tx(_tx_hash = transaction["tx_hash"])
#             tx = json.loads(tx)
#             vin = tx["vin"]
#             return True
#         except Exception as e:
#             print("Error: {e}")
#             return False 

#     @property
#     def values(self):
#         return [self.redis.get(key) for key in self.redis.scan_iter()]

#     @property
#     def items(self):
#         return [[key.decode(), self.redis.get(key).decode()] for key in self.redis.scan_iter()]

#     def __iter__(self):
#         for key in self.redis.scan_iter():
#             yield key.decode()

