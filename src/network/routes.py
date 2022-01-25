from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from transaction.transaction import Transaction
from transaction.transaction_in import TransactionInput
from transaction.transaction_out import TransactionOutput
from wallet.wallet import Wallet
network = Blueprint("network", __name__)

@network.route("/transaction", methods=["POST"])
@login_required
def create_transaction(self):
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400

    txin_list = []
    for last_tx_id, last_txout_idx in request.form.txins:
        txin_list.append(TransactionInput(last_tx_id, last_txout_idx))
    
    txout_list = []
    for amount, address in request.form.txins:
        public_hashed_key = Wallet.address_to_public_hashed_hash(address)
        txout_list.append(TransactionOutput(amount, public_hashed_key))
    transaction = Transaction(txin_list, txout_list)


@network.route("/broadcast-transaction")
def broadcast_transaction():
    request_data = request.get_json()
    if not request_data:
        response = {'message': 'data is missing'}
        return jsonify(response), 400
    required = ['sender', 'recipient', 'amount', 'signature']

@network.route("/broadcast-block")
def broadcast_block():
    pass

