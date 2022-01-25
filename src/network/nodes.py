import os, json
import sqlite3 
from copy import deepcopy
import requests
from flask_login import login_manager, UserMixin

BASE_DIR = os.path.dirname(__file__)
user_db = lambda db_name: os.path.join(BASE_DIR, db_name)

class Node:
    def __init__(self, hostname, address):
        self.hostname = hostname
        self.address = address
        self.url = f"http:{hostname}"

    def __eq__(self, other):
        return self.hostname == other.hostname

    def get(self, endpoint):
        url = os.path.join(self.url, endpoint)
        request_data = requests.get(url)
        return request_data
    
    def post(self, endpoint, data = None):
        url = os.path.join(self.url, endpoint)
        request_data = requests.get(url, json=data)
        return request_data

    def to_dict(self):
        return deepcopy({
            "hostname": self.hostname,
            "address": self.address
        })

    def to_json(self):
        return json.dumps(self.to_dict())

# class NodeDatabase:
#     def __init__(self, file_name):
#         self.file_path = os.path.join(BASE_DIR, file_name)
#         self.node_list = []

#     def save(self):
#         with open(self.file_path, mode="w") as file:
#             file.write([node.to_json() for node in self.node_list])

#     def load(self):
#         with open(self.file_path, mode="w") as file:
#             nodes = file.read()
#         for node in nodes:
#             self.node_list.append(Node(**json.loads(node)))

#     def add(self, node):
#         self.node_list.append(node)
#         self.save()

class User(UserMixin):
    def __init__(self, private_key, public_key, address):
        self.private_key = private_key 
        self.public_key = public_key 
        self.address = address 
        
# @login_manager.user_loader 
# def load_user(_private_key):
#     try:
#         wallet = Wallet(_private_key)
#         return User(**wallet.get())
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

class Node:
    def __init__(self, db_name):
        if os.path.isfile(user_db(db_name)):
            self.con = sqlite3.connect(user_db(db_name))
            print(f"[*] Connected to {db_name}")
        else:
            file_name = open(user_db(db_name), mode="w").close()
            self.con = sqlite3.connect(file_name)
            print(f"[*] Create and Connected to {db_name}")
        
        self.cursor = self.con.cursor()
        self.__create_table(self)

    def __create_table(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS user")
        self.con.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (hostname STRING, address STRING DEFAULT 'unknown') 
        """)

    def save_one(self, hostname, address=None):
        self.cursor.execute("""
        INSERT VALUE user (hostname, address) values (?, ?)
        """, hostname, address)
        self.con.commit()

    # def save_many(self, data):
    #     self.cursor.execute("""
    #     INSERT VALUE user (address, url) values (?, ?)
    #     """, user, url)

    def get_one(self, hostname):
        self.cursor.execute("""
        SELECT * FROM user WHERE hostname = ?
        """, hostname)
        return self.cursor.fetchone()

    def get_all(self):
        self.cursor.execute("""
        SELECT * FROM user
        """)
        return self.cursor.fetchall()