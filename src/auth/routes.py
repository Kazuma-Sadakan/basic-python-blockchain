from flask import Blueprint, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from src.network.node_db import save_one, get_one
from src.wallet.wallet import Wallet
from .auth import User

auth = Blueprint("auth", __name__)

HOST = "localhost"
PORT = 3000
URL = f"{HOST}:{PORT}"

@auth.route("/wallet/create", methods=["POST"])
def create_wallet():
    try:
        wallet = Wallet(wallet_id = URL)
        # save_one(wallet.wallet_id, wallet.address)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'address': wallet.address,
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
    
    if not request_data:
        response = {
            "message": "Data not found"
        }
        return jsonify(response), 500

    elif "private_key" not in request_data:
        response = {
            "message": "Private key not found"
        }
        return jsonify(response), 400

    try:
        wallet = Wallet(wallet_id = URL, private_key = request_data["private_key"])
    except Exception as e:
        print(f"Error: {e}")
        response = {
            "message": "The private key does not exist."
        }
        return jsonify(response), 400

    try:
        if wallet.address:
            response = {
                'public_key': wallet.public_key,
                'private_key': wallet.private_key,
                'address': wallet.address,
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


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    response = {
        "message": "logged out"
    }
    return jsonify(response), 200
