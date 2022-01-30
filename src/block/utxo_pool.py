import json, pickle
import pymongo
from pymongo import MongoClient
# from bson.objectid import ObjectId
import os 
import pickle

HOST = 'localhost'
PORT = 27017
url = ""
DB_NAME = "utxo"
COLLECTION_NAME = "utxo"

try:
    if url:
        client = MongoClient(url)
    else:
        client = MongoClient(host = HOST, port = PORT)
except pymongo.errors.ConnectionFailure as e:
    print(e)

if DB_NAME in client.list_database_names():
    print(f"[*]Connect to {DB_NAME}")
    db = client[DB_NAME]
else:
    print(f"[*]{DB_NAME} created")
    db = client[DB_NAME]

collection = db[COLLECTION_NAME]


def save_one(_address:str, _data:str):
    try:
        if not collection.find({"address": _address}).count():
            collection.insert_one({"address": _address, "unspent_outputs": [_data]})
        else:
            collection.update_one({"address": _address}, {"$push": {"unspent_outputs": _data}})
        print(f"Saving address: {_address}, utxo: {_data} success")
        return True
    except Exception as e:
        print(f"Saving address: {_address}, utxo: {_data} failed")
        print(f"Error: {e}")
        return False 

def save_many(_address:str, _data_list:list):
    try:
        if not collection.find(filter={"address": _address}).count():
            collection.insert_one({"address": _address, "unspent_outputs": _data_list})
        else:
            # for data in data_list:
            collection.update_one({"address": _address}, {"$push": {"unspent_outputs": {"$each": _data_list}}})
        print(f"Saving address: {_address}, utxo: {_data_list} success")
        return True
    except Exception as e:
        print(f"Saving address: {_address}, utxo: {_data_list} success")
        print(f"Error: {e}")
        return False 

def remove_one(_address, _tx_hash, _tx_output_n):
    collection.update_one({"address": _address}, \
        {"$pull": {"unspent_outputs": {"tx_hash": _tx_hash, "tx_output_n": _tx_output_n}}})

def remove_many(_address, keys):
    for key in keys:
        remove_one(_address = _address, _tx_hash = key["tx_hash"], _tx_output_n = key["tx_output_n"])

def get_utxos(_address):
    return collection.find_one(filter = {"address": _address})['unspent_outputs']

def get_utxo(address, tx_hash, tx_output_n) -> dict:
    for doc in collection.find({"address": address}, 
                                {"unspent_outputs": {"$elemMatch": {"tx_hash": tx_hash, 
                                                                    "tx_output_n": tx_output_n}}}):
        return doc['unspent_outputs']


def get_all():
    for doc in collection.find():
        return doc




# class UtxoDB:
#     def __init__(self, _host=None, _port=None, _url=None):
#         try:
#             self.client = MongoClient(_url) if _url else MongoClient(host = _host, port = _port)
#         except Exception as e:
#             print(f"Error: {e}")

#     def connect_db(self, _db_name):
#         if _db_name in self.client.list_database_names():
#             print(f"[*]Connect to {_db_name}")
#             self.db = self.client[_db_name]
#         else:
#             print(f"[*]{_db_name} created")
#             self.db = self.client[_db_name]

#     def connect_collection(self, _name):
#         self.collection = self.db[_name]

#     def save_one(self, address, data):
#         try:
#             if not self.collection.find_one(filter={"address": address}):
#                 self.collection.insert_one({"address": address, "unspent_outputs": [data]})
#             else:
#                 self.collection.update_one({"address": address}, {"$push": {"unspent_outputs": data}})
#             print(f"Saving address: {address}, utxo: {data} success")
#             return True
#         except Exception as e:
#             print(f"Saving address: {address}, utxo: {data} failed")
#             print(f"Error: {e}")
#             return False 

#     def save_many(self, address, data_list):
#         try:
#             if not self.collection.find_one(filter={"address": address}):
#                 self.collection.insert_one({"address": address, "unspent_outputs": data_list})
#             else:
#                 # for data in data_list:
#                 self.collection.update_one({"address": address}, {"$push": {"unspent_outputs": {"$each": data_list}}})
#             print(f"Saving address: {address}, utxo: {data_list} success")
#             return True
#         except Exception as e:
#             print(f"Saving address: {address}, utxo: {data_list} success")
#             print(f"Error: {e}")
#             return False 

#     def remove_one(self, address, tx_hash, tx_output_n):
#         self.collection.update_one({"address": address}, \
#             {"$pull": {"unspent_outputs": {"tx_hash": tx_hash, "tx_output_n": tx_output_n}}})

#     def remove_many(self, address, keys):
#         for key in keys:
#             self.remove_one(address, key["tx_hash"], key["tx_output_n"])

#     def get_utxos(self, _address):
#         return self.collection.find_one(filter = {"address": _address})['unspent_outputs']

#     def find_utxo(self, _address, _tx_hash, _tx_output_n) -> dict:
#         for doc in self.collection.find({"address": _address}, {"unspent_outputs": {"$elemMatch": {"tx_hash": _tx_hash, "tx_output_n": _tx_output_n}}}):
#             return doc['unspent_outputs']

#     @property
#     def items(self):
#         for utxo in self.collection.find():
#             yield utxo["address"], utxo['unspent_outputs']

#     def __iter__(self):
#         for utxos in self.collection.find():
#             for utxo in utxos['unspent_outputs']:
#                 yield utxo["tx_hash"]

    