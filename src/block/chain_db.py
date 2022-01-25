import json, pickle
from pymongo import MongoClient
from bson.objectid import ObjectId

import os 
from wallet.wallet import Wallet 
import pickle

class ChainDatabase:
    def __init__(self, _host=None, _port=None, url=None):
        try:
            self.client = MongoClient(url) if url is not None else MongoClient(host = _host, port = _port)
        except Exception as e:
            print(f"Error: {e}")

    def connect_db(self, db_name):
        if db_name in self.client.list_database_names():
            print(f"[*]Connect to {db_name}")
            self.db = self.client[db_name]
        else:
            print(f"[*]{db_name} created")
            self.db = self.client[db_name]

    def connect_collection(self, name):
        self.collection = self.db[name]

    def save_one(self, data):
        try:
            request_data = self.collection.insert_one(data)
            return True

        except Exception as e:
            print(f"Error: {e}")
            return False 

    def save_many(self, projection = None, filter = None, sort = None):
        try:
            self.collection.insert_one(projection = projection, filter = filter, sort = sort)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False 
            
    def get_all(self):
        try:
            for data in self.collection.find():
                yield data
        except Exception as e:
            print(f"Error: {e}")  
            return -1

    def find_one_by_id(self, id):
        return self.collection.find_one(filter = {"_id": ObjectId(id)})

    def find_one_by_hash(self, hash):
        return self.collection.find_one(filter = {'header': {"block_hash": hash}})


        


# mongo = MongoDatabase("localhost", 27017)
# mongo.connect_db("blockchain")
# mongo.connect_collection("chain")
# # mongo.save_one({'index': 0, 'header': {'prev_block_hash': 'a85fec56edcd23dbef2311d1057a044a91e10996aa1275029b40a0c58bed22fb', 'merkle_root': '98a861ec4983e3562f38168b276e0edf63afcbb2503ace3a5a226c0de2048a4b', 'nonce': 0, 'difficulty': 3, 'timestamp': 1642825349.946898, 'block_hash': '7482fc1de65af18b86a2de65232c10ccabbbbde250bb007743002eb88f60c4df'}, 'tx_list': [{'id': 0, 'txin_list': [{'last_tx_id': 13, 'last_txout_idx': 0, 'script_sig': '12345\t54321'}, {'last_tx_id': 12, 'last_txout_idx': 1, 'script_sig': ''}], 'txout_list': [{'value': 100, 'script_pubkey': 'OP_DUP\tOP_HASH160\t123\tOP_EQUALVERIFY\tOP_CHECKSIG'}, {'value': 200, 'script_pubkey': 'OP_DUP\tOP_HASH160\t234\tOP_EQUALVERIFY\tOP_CHECKSIG'}]}, {'id': 0, 'txin_list': [{'last_tx_id': 13, 'last_txout_idx': 0, 'script_sig': '12345\t54321'}, {'last_tx_id': 12, 'last_txout_idx': 1, 'script_sig': ''}], 'txout_list': [{'value': 100, 'script_pubkey': 'OP_DUP\tOP_HASH160\t123\tOP_EQUALVERIFY\tOP_CHECKSIG'}, {'value': 200, 'script_pubkey': 'OP_DUP\tOP_HASH160\t234\tOP_EQUALVERIFY\tOP_CHECKSIG'}]}]})
# # print(mongo.find_one_by_id('61eb86e78c6614e0da846442'))
# print(mongo.find_one_by_hash('7482fc1de65af18b86a2de65232c10ccabbbbde250bb007743002eb88f60c4df'))