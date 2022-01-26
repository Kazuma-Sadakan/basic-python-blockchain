import time
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.utils.constants import DIFFICULTY
from src.transaction.transaction import Transaction
from src.transaction.transaction_in import TransactionInput
from src.transaction.transaction_out import TransactionOutput
from src.block.block import BlockHead, Block
from src.utils.proof_of_work import ProofOfWork
from src.block.memory_pool  import Mempool
from src.block.chain import Blockchain
from src.wallet.wallet import Wallet
from src.utils.utils import MerkleTree
from src.block.utxo_pool import UtxoDB
from src.wallet.wallet import Wallet

network = Blueprint("network", __name__)

db = UtxoDB('localhost', 27017)
db.connect_db("utxo")
db.connect_collection("utxo")

mempool = Mempool("localhost", 6379)
blockchain = Blockchain()

@network.route("/transaction", methods=["POST"])
@login_required
def create_transaction(self):
    request_data  = request.get_json()
    if not request_data:
        response = {
            "message": "No data found."
        }
        return jsonify(response), 400

    print(request_data)

# @network.route("/transaction", methods=["POST"])
# @login_required
# def create_transaction(self):
#     values = request.get_json()
#     if not values:
#         response = {
#             'message': 'No data found.'
#         }
#         return jsonify(response), 400

#     txin_list = [] 
#     utxos = [db.find_utxo(adddress, tx_hash, tx_output_n) for tx_hash, tx_output_n in request.form.txin_list]
#     for utxo in utxos:
#         txin_list.append(TransactionInput())
    
#     txout_list = []
#     for amount, address in request.form.txins:
#         public_hashed_key = Wallet.address_to_public_hashed_hash(address)
#         txout_list.append(TransactionOutput(amount, public_hashed_key))
#     transaction = Transaction(txin_list, txout_list)

# @network.route("/broadcast-transaction")
# def broadcast_transaction():
#     request_data = request.get_json()
#     if not request_data:
#         response = {'message': 'data is missing'}
#         return jsonify(response), 400
#     required = ['sender', 'recipient', 'amount', 'signature']

# @network.route("/mining")
# def mining():
#     tx_list = [Transaction.load(**tx) for tx in mempool.get_all()]
#     previous_block_hash = blockchain.last_block.head.block_hash
#     tx_hash_list = [tx.tx_hash for tx in tx_list]
#     merkle_root_hash = MerkleTree.generate_merkle_root(tx_hash_list)
#     block_head = BlockHead(version = 0, 
#              previous_block_hash = previous_block_hash, 
#              merkle_root_hash = merkle_root_hash, 
#              difficulty = DIFFICULTY,
#              nonce = 0)

#     block = Block(tx_list = tx_list, block_head = block_head)


# @network.route("/broadcast-block")
# def broadcast_block():
#     for i in range(self.)
#     previous_block = 
#     current_block 

