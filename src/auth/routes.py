from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from src.network.node_db import NodeDB
from src.wallet.wallet import Wallet
from .auth import User
node = NodeDB("nodes.db")
auth = Blueprint("auth", __name__)

@auth.route("/wallet/create", methods=["POST"])
def create_wallet():
    if request.method == "POST":
        try:
            wallet = Wallet(wallet_id = 5000)
            response = {
                'public_key': wallet.public_key,
                'private_key': wallet.private_key,
                'address': wallet.address,
                'balance': ""
            }
            print(wallet.address)
            node.save_one(3000, wallet.address)
            return jsonify(response), 201
        except Exception as e:
            print(f"Error: {e}")
            response = {
                'message': 'Creating a wallet failed.'
            }
            return jsonify(response), 500

@auth.route("/wallet/load", methods=["POST"])
def load_wallet():
    if request.method == "POST":
        request_data = request.get_json()
        try:
            wallet = Wallet(wallet_id = 5000, private_key = request_data["password"])
            
        except Exception as e:
            print(f"Error: {e}")
        try:
            if node.get_one(wallet.address):
                response = {
                    'public_key': wallet.public_key,
                    'private_key': wallet.private_key,
                    'address': wallet.address,
                    'balance': ""
                }
                user = User(*wallet.get())
                login_user(user)
                return jsonify(response), 201
        except Exception as e:
            print(f"Error: {e}")
            response = {
                'message': "Loading a wallet failed"
            }
            return jsonify(response)

