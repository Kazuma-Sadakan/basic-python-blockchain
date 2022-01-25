import json, pickle
from pymongo import MongoClient
# from bson.objectid import ObjectId
import os 
import pickle

class UtxoDB:
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

    def save_one(self, address, data):
        try:
            if not self.collection.find_one(filter={"address": address}):
                self.collection.insert_one({"address": address, "unspent_outputs": [data]})
            else:
                self.collection.update_one({"address": address}, {"$push": {"unspent_outputs": data}})
            print(f"Saving address: {address}, utxo: {data} success")
            return True
        except Exception as e:
            print(f"Saving address: {address}, utxo: {data} failed")
            print(f"Error: {e}")
            return False 

    def save_many(self, address, data_list):
        try:
            if not self.collection.find_one(filter={"address": address}):
                self.collection.insert_one({"address": address, "unspent_outputs": data_list})
            else:
                for data in data_list:
                    self.collection.update_one({"address": address}, {"$push": {"unspent_outputs": data}})
            print(f"Saving address: {address}, utxo: {data_list} success")
            return True
        except Exception as e:
            print(f"Saving address: {address}, utxo: {data_list} success")
            print(f"Error: {e}")
            return False 

    def remove_one(self, address, tx_hash, tx_output_n):
        self.collection.update_one({"address": address}, \
            {"$pull": {"unspent_outputs": {"tx_hash": tx_hash, "tx_output_n": tx_output_n}}})

    def remove_many(self, address, keys):
        for key in keys:
            self.remove_one(address, key["tx_hash"], key["tx_output_n"])

    def get_utxos(self, address):
        return self.collection.find_one(filter = {"address": address})['unspent_outputs']

    def find_utxo(self, address, tx_hash, tx_output_n):
        for doc in self.collection.find({"address": address}, {"unspent_outputs": {"$elemMatch": {"tx_hash": tx_hash, "tx_output_n": tx_output_n}}}):
            return doc['unspent_outputs']

    def find_utxos(self, address, keys):
        utxo_list = []
        for tx_hash, tx_output_n in keys:
            utxo_list.append(self.find_utxo(address, tx_hash, tx_output_n))
        return utxo_list

    @property
    def items(self):
        for utxo in self.collection.find():
            yield utxo["address"], utxo['unspent_outputs']

    def __iter__(self):
        for utxos in self.collection.find():
            for utxo in utxos['unspent_outputs']:
                yield utxo["tx_hash"]

    