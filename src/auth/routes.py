from flask import Blueprint, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from src.network.node_db import NodeDB
from src.wallet.wallet import Wallet
from .auth import User


node_db = NodeDB("nodes.db")
auth = Blueprint("auth", __name__)

HOST = "localhost"
PORT = 3000
URL = f"{HOST}:{PORT}"

@auth.route("/wallet/create", methods=["POST"])
def create_wallet():
    try:
        wallet = Wallet(wallet_id = URL)
        node_db.save_one(wallet.wallet_id, wallet.address)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'address': wallet.address,
            'balance': ""
        }
        return jsonify(response), 201
    except Exception as e:
        print(f"Error: {e}")
        response = {
            'message': 'Creating a wallet failed.'
        }
        return jsonify(response), 500

@auth.route("/wallet/load", methods=["POST"])
def load_wallet():
    request_data = request.get_json()
    try:
        wallet = Wallet(wallet_id = URL, private_key = request_data["private_key"])
        
    except Exception as e:
        print(f"Error: {e}")
    try:
        if node_db.get_one(wallet.address):
            response = {
                'public_key': wallet.public_key,
                'private_key': wallet.private_key,
                'address': wallet.address,
                'balance': ""
            }
            user = User(**wallet.get())
            login_user(user)
            return jsonify(response), 201
    except Exception as e:
        print(f"Error: {e}")
        response = {
            'message': "Loading a wallet failed"
        }
        return jsonify(response), 500


