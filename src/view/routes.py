from cmath import log
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from wallet.wallet import Wallet
view = Blueprint("view", __name__, template_folder="../templates/view")

@view.route("/node", methods = ["GET"])
@view.route("/")
def node():

    return render_template("node.html")
    

@view.route("/balance", methods=["GET"])
@login_required
def balance():
    try:
        current_user.address
        balance = ""
        response = {
            'message': 'Fetched balance successfully.',
            'balance': balance
        }
        return jsonify(response), 200
    except Exception as e:
        print(f"Error: {e}")
        response = {
            'messsage': 'Loading balance failed.',
        }
        return jsonify(response), 500


@view.route("/wallet/balance", methods=["GET"])
def balance():
    pass

@view.route("/transaction", methods=["POST"])
def transaction():
    pass


