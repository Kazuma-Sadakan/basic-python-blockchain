import time, requests
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.block import memory_pool
from src.transaction.verification import Verification
from src.utils.constants import DIFFICULTY, MINING_REWARD
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
from src.utils.utils import create_transaction_input
from src.network.node_db import NodeDB
from src.network.nodes import Node

network = Blueprint("network", __name__)

utxo_db = UtxoDB('localhost', 27017)
utxo_db.connect_db("utxo")
utxo_db.connect_collection("utxo")

mempool = Mempool("localhost", 6379)

blockchain = Blockchain()
blockchain.load()

nodedb = NodeDB("nodes.db")
node_list = []
for hostname, address in nodedb.get_all():
    node_list.append(Node(hostname=hostname, address=address))

@network.route("/chain", methods=["GET"])
def get_chain():
    return jsonify({"chain": blockchain.chain}), 200

@network.route("/transaction", methods=["POST"])
@login_required
def create_transaction():
    request_data  = request.get_json()
    if not request_data:
        response = {
            "message": "Data not found."
        }
        return jsonify(response), 400

    # request_data = 
    # {"utxos": [
    # "tx_hash" + "tx_output_n"
    # "111123dde201bc37db7dc57e0cb6243a875f3d0c799664d0a311c83633d2dbaf" + "0"
    # "72b950d2a37ffaf7b595a84acd976875d84e82c00bfa47ff50aea0e827f5b8c4" + "0"
    # ],
    # send: [
    # { value: 1,
    #   address: ""},
    # { value: 2
    #   address: ""}
    # ],
    # "locktime": 0,
    # }
    utxos = [utxo_db.find_utxo(current_user.address, utxo[: 64], utxo[64: ]) for utxo in request_data["utxos"]]
    if not all(utxos):
        response = {
            "message": "utxos you have requested do not exist"
        }
        return jsonify(response), 400

    txin_list = []
    for utxo in utxos:
        previous_tx = blockchain.get_tx(block_height = utxo["block_height"], tx_hash = utxo["tx_hash"]) 
        txin = create_transaction_input(current_user.private_key, 
                                        current_user.public_key, 
                                        previous_transaction = previous_tx, 
                                        tx_hash = utxo["tx_hash"], 
                                        tx_output_n = utxo["tx_output_n"])
        txin_list.append(txin)

    txout_list = []
    for value, next_owner_address in request_data["send"]:
        txout_list.append(TransactionOutput(value = value,
                                            address = next_owner_address))

    transaction = Transaction(_vin = txin_list, 
                              _vout= txout_list,
                              _version=0,
                              _locktime = request_data["locktime"])

    verification = Verification(transaction.to_dict())
    if verification.in_mempool():
        return jsonify({"message": "The requested transaction has already been in process"}), 400

    elif not verification.valid_funds(current_user.address):
        return jsonify({"message": "The fund is not enough"}), 400

    elif not verification.success_unlock(current_user.address):
        return jsonify({"message": "The utxos are not valid"}), 400

    elif mempool.add_tx(transaction.tx_hash, transaction.to_json()):
        for node in node_list:
            try:
                data = {"transaction": transaction.to_dict(),
                        "sender": {"hostname": hostname, 
                                "address": address} 
                }
                response = node.post("/broadcast-transaction", data)
                if response.status_code == 400 or response.status_code == 500:
                    return jsonify({"message": 'Transaction declined.'}), 400

            except requests.exceptions.ConnectionError:
                    return jsonify({"message": "Transaction Error"}), 400
   
@network.route("/broadcast-transaction", methods=["POST"])
def broadcast_transaction():
    request_data = request.get_json()
    if not request_data:
        response = {'message': 'data is missing'}
        return jsonify(response), 400
    try:
        transaction = Transaction.load(request_data["transaction"])
    except Exception as e:
        print(f"Error: {e}")
        response = {'message': 'Some data is missing'}
        return jsonify(response), 400

    verification = Verification(transaction.to_dict())
    if verification.in_mempool():
        return jsonify({"message": "The requested transaction has already been in process"}), 400

    if not verification.valid_funds(request_data["address"]):
        return jsonify({"message": "The fund is not enough"}), 400

    if not verification.success_unlock(request_data["address"]):
        return jsonify({"message": "The utxos are not valid"}), 400

    mempool.set(transaction.tx_hash, transaction.to_json())
    for node in node_list:
        try:
            response = node.post("/broadcast-transaction", request_data)
            if response.status_code == 400 or response.status_code == 500:
                print('Transaction declined, needs resolving')
                return False

        except requests.exceptions.ConnectionError:
            response = {
                "message": "Transaction Error"
                }
            return jsonify(response), 400
    

@network.route("/mining")
def mining():
    tx_list = [Transaction.load(**tx) for tx in mempool.get_all()]
    previous_block_hash = blockchain.last_block.head.block_hash
    tx_hash_list = [tx.tx_hash for tx in tx_list]
    merkle_root_hash = MerkleTree.generate_merkle_root(tx_hash_list)
    timestamp = time.time()

    nonce = ProofOfWork.get_nonce(merkle_root_hash = merkle_root_hash, 
                                previous_block_hash = previous_block_hash,
                                difficulty = DIFFICULTY, 
                                timestamp = timestamp)

    block_head = BlockHead(version = 0, 
             previous_block_hash = previous_block_hash, 
             merkle_root_hash = merkle_root_hash, 
             difficulty = DIFFICULTY,
             nonce = nonce,
             timestamp = timestamp)

    coinbase_transaction = Transaction(vin=[], vout=[TransactionOutput(MINING_REWARD, current_user.address)])
    tx_list.insert(0, coinbase_transaction)
    block = Block(tx_list = tx_list, block_head = block_head)
    block_dict = block.to_dict()
    blockchain.add_block(block_dict)
    mempool.remove_all()
    for node in node_list:
        try:
            response = node.post("/broadcast-block", {"block": block_dict})
            if response.status_code == 400 or response.status_code == 500:
                print('Block declined')
            # if response.status_code == 409:
            #     self.resolve_conflicts = True
        except requests.exceptions.ConnectionError:
            continue
    return jsonify({"block": block.to_dict()}), 201

@network.route("/broadcast-block", methods=["POST"])
def broadcast_block():
    request_data = request.get_json()
    if not request_data:
        response = {'message': 'No data found.'}
        return jsonify(response), 400
    if 'block' not in request_data:
        response = {'message': 'Some data is missing.'}
        return jsonify(response), 400
    block = request_data['block']
    if not blockchain.verify_chain():
        response = {'message': 'local blockchain is not valid.'}
        return jsonify(response), 400
    for node in node_list:
        chain = node.get("/chain")
        
        longest_chain = blockchain.chain[:]
        if len(longest_chain) < len(chain):
            pass

@network.route("/node", methods = ["GET"])
@network.route("/")
def node():
    return render_template("node.html")
    

@network.route("/balance", methods=["GET"])
@login_required
def balance():
    try:
        utxos = db.find_utxos(address = current_user.address)
        balance = sum([utxo["value"] for utxo in utxos])
        response = {
            'balance': balance
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error: {e}")
        response = {
            'messsage': 'Loading balance failed.',
        }
        return jsonify(response), 500




