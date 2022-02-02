import json
import os
import redis
import sys
import logging
from .utxo_pool import get_utxo

HOST = os.environ.get("localhost")
PORT = os.environ.get("port")
DB = 0

logging.basicConfig(filename="test.log", level=logging.DEBUG, 
                    format="%(asctime)s:%(levelname)s:%(message)s")
try:
    mempool = redis.Redis(host = HOST, 
                          port = PORT, 
                          db = DB,
                          charset = "utf-8", 
                          decode_responses = True)
except redis.ConnectionError as e:
    logging.critical("redis Connection Error")
    sys.exit(1)

def add_tx(tx_hash:str, transaction:str) -> bool:
    try:
        if mempool.exists(tx_hash):
            return False 
        success = mempool.set(tx_hash, transaction)
    except Exception as e:
        logging.error(f"add_tx: {e}")
        sys.exit(1)
    return success

def get_tx(tx_hash:str) -> dict:
    try:
        data = mempool.get(tx_hash)
    except Exception as e:
        logging.critical(f"get_tx: {e}")
        sys.exit(1)
    if data is None:
        return {}
    else:
        return json.loads(data)

def get_all() -> list:
    tx_list = []
    for tx_hash in mempool.keys():
        try:
            tx = get_tx(tx_hash = tx_hash)
            if bool(tx):
                raise ValueError("Transaction not found.")
        except Exception as e:
            logging.critical(f"get_all: {e}")
            sys.exit(1)
        tx_list.append(json.loads(tx))
    return tx_list
    
def delete_tx(tx_hash:str) -> bool:
        try:
            success = mempool.delete(tx_hash)
        except Exception as e:
            logging.critical(f"delete_tx: {e}")
            sys.exit(1)
        return success

def delete_all() -> bool:
    for tx_hash in mempool.keys():
        success = delete_tx(tx_hash = tx_hash)
        if not success:
            logging.error(f"delete_all: {e}")
            return False 
    return True

def get_keys():
    for key in mempool.keys():
        yield key 

def tx_exists(tx_hash:str) -> bool:
    try:
        exist = mempool.exists(tx_hash)
    except Exception as e:
        logging.error(f"tx_exists: {e}")
        sys.exit(1)
    return exist

def tx_out_exists(tx_hash:str, tx_output_n:int) -> bool:
    tx = get_tx(tx_hash = tx_hash)
    if bool(tx):
        return False
    vout = tx["vout"]
    try:
        tx_out = vout[tx_output_n]
    except IndexError as e:
        logging.error(f"tx_out_exists: {e}")
        return False 
    return True

def tx_in_exists(address, tx_hash, tx_output_n) -> bool:
    transaction = get_utxo(address = address, 
                               tx_hash = tx_hash, 
                               tx_output_n = tx_output_n)
    if bool(transaction):
        return False
    try:
        tx = get_tx(tx_hash = transaction["tx_hash"])
    except logging.error(f"tx_out_exists: {e}"):
        return True

    try:
        vin = tx["vin"]
    except KeyError as e:
        logging.error(f"tx_out_exists: {e}")
        return True


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

