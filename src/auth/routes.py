from tkinter.messagebox import NO
from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_user, logout_user, login_required
from itsdangerous import exc
from wallet.wallet import Wallet
from database import NodeDatabase
auth = Blueprint("auth", __name__)
node = NodeDatabase("nodes")


    

@auth.route("/wallet/create", methods=["POST"])
def create_wallet():
    if request.method == "POST":
        try:
            wallet = Wallet()
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
    if request.method == "POST":
        try:
            wallet = Wallet(request.form.password)
        except Exception as e:
            print(f"Error: {e}")
        try:
            if node.get_one(wallet.address):
                response = {
                    'public_key': wallet.public_key,
                    'private_key': wallet.private_key,
                    'address': wallet.adddress,
                    'balance': ""
                }
                return jsonify(response), 201
        except Exception as e:
            print(f"Error: {e}")
            response = {
                'message': "Loading a wallet failed"
            }
            return jsonify(response)

@auth.route("/mine", methods=["GET", "POST"])
@login_required
def mine():
    pass
