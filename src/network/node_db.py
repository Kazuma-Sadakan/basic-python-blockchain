import os, json
import sqlite3 
from copy import deepcopy
from flask_login import login_manager, UserMixin

BASE_DIR = os.path.dirname(__file__)
user_db = lambda db_name: os.path.join(BASE_DIR, db_name)

class NodeDB:
    def __init__(self, db_name):
        if os.path.isfile(user_db(db_name)):
            self.con = sqlite3.connect(user_db(db_name), check_same_thread=False)
            print(f"[*] Connected to {db_name}")
        else:
            open(user_db(db_name), mode="w").close()
            self.con = sqlite3.connect(user_db(db_name), check_same_thread=False)
            print(f"[*] Create and Connected to {db_name}")
        
        self.cursor = self.con.cursor()
        self.__create_table()

    def __create_table(self):
        # self.cursor.execute("CREATE DATABASE IF NOT EXISTS user")
        # self.con.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (hostname STRING, address STRING DEFAULT 'unknown') 
        """)
        self.con.commit()

    def save_one(self, hostname, address=None):
        
        self.cursor.execute("""
        INSERT INTO user (hostname, address) VALUES  (:hostname, :address)
        """, {"hostname": hostname, "address": address})
        self.con.commit()

    # def save_many(self, data):
    #     self.cursor.execute("""
    #     INSERT VALUE user (address, url) values (?, ?)
    #     """, user, url)

    def get_one(self, address):
        self.cursor.execute("""
        SELECT * FROM user WHERE address = (:address)
        """, {"address": address})
        return self.cursor.fetchone()

    def get_all(self):
        self.cursor.execute("""
        SELECT * FROM user
        """)
        return self.cursor.fetchall()