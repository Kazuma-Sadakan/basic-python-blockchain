import json
import pickle
import os, sys
import pickle
import logging 

import pymongo
from pymongo import MongoClient

logging.basicConfig(filename="test.log", level=logging.DEBUG, 
                    format="%(asctime)s:%(levelname)s:%(message)s")

HOST = os.environ.get("host")
PORT = os.environ.get("port")
url = os.environ.get("mongo_url", None)

DB_NAME = "utxo"
COLLECTION_NAME = "utxo"

try:
    if url is not None:
        client = MongoClient(url)
    else:
        client = MongoClient(host = HOST, port = PORT)
except pymongo.errors.ConnectionFailure as e:
    logging.critical("mongodb ConnectionFailure")

if DB_NAME in client.list_database_names():
    logging.info(f"Connect to {DB_NAME}")
    db = client[DB_NAME]
else:
    logging.info(f"{DB_NAME} created")
    db = client[DB_NAME]

collection = db[COLLECTION_NAME]

def save_one(address:str, data:str) -> bool:
    try:
        if not collection.find({"address": address}).count():
            collection.insert_one({"address": address, "unspent_outputs": [data]})
        else:
            collection.update_one({"address": address}, {"$push": {"unspent_outputs": data}})
        return True
    except Exception as e:
        logging.error(f"utxo save_one Error: {e}")
        return False 

def save_many(address:str, data_list:list) -> bool:
    try:
        if not collection.find(filter={"address": address}).count():
            collection.insert_one({"address": address, "unspent_outputs": data_list})
        else:
            collection.update_one({"address": address}, {"$push": {"unspent_outputs": {"$each": data_list}}})
        return True
    except Exception as e:
        logging.error(f"utxo save_one Error: {e}")
        return False 

def remove_one(address, tx_hash, tx_output_n) -> bool:
    try:
        collection.update_one({"address": address}, 
                              {"$pull": {"unspent_outputs": {"tx_hash": tx_hash, "tx_output_n": tx_output_n}}})
        return True
    except Exception as e:
        logging.error(f"utxo remove_one Error: {e}")
        return False

def get_utxos(address):
    return collection.find_one(filter = {"address": address})['unspent_outputs']

def get_utxo(address, tx_hash, tx_output_n) -> dict:
    data = collection.find_one(filter = {"address": address},
           projection = {"unspent_outputs": {"$elemMatch": {"tx_hash": tx_hash, "tx_output_n": int(tx_output_n)}}})
    if bool(data):
        return {} 
    else: return data['unspent_outputs'][0]

def get_all():
    return list(collection.find())

def delete_all():
    try:
        collection.remove({})
        return True
    except Exception as e:
        logging.error("utxo delete_all failed")
        return False


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

    