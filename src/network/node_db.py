import os, json
import sqlite3 
from typing import List
from copy import deepcopy
from flask_login import login_manager, UserMixin

BASE_DIR = os.path.dirname(__file__)
user_db = lambda db_name: os.path.join(BASE_DIR, db_name)

def init_node():
    global con, cursor
    if os.path.isfile(user_db("node.db")):
        con = sqlite3.connect(user_db("node.db"), check_same_thread=False)
        print(f"[*] Connected to node.db")
    else:
        open(user_db("node.db"), mode="w").close()
        con = sqlite3.connect(user_db("node.db"), check_same_thread=False)
        print(f"[*] Create and Connected to node.db")

    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (hostname STRING, address STRING UNIQUE) 
    """) 
    con.commit() 

init_node()

def save_one(hostname:str, address:str):
    try:
        cursor.execute("""
        INSERT INTO user (hostname, address) VALUES (:hostname, :address)
        """, {"hostname": hostname, "address": address})
        con.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    return False

def save_many(data:list):
    try:
        cursor.executemany("""
        INSERT INTO user (hostname, address) VALUES (?, ?)
        """, data)
        con.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    return False

def delete_one(address):
    try:
        cursor.execute("""
        DELETE FROM user WHERE address = (:address)
        """, {"address": address})
        con.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    return False

def get_one(address):
    cursor.execute("""
    SELECT * FROM user WHERE address = (:address)
    """, {"address": address})
    return cursor.fetchone()

def get_all():
    cursor.execute("""
    SELECT * FROM user
    """)
    return cursor.fetchall()