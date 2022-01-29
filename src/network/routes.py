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
from src.utils.utils import create_transaction_input, create_script_sig
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
    try:
        response = {
            "chain": blockchain.chain
            }
        return jsonify(response), 200
    except Exception as e:
        print(f"Error: {e}")
        response = {
            "message": "blockchain not found"
            }
        return jsonify(response), 400

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
    # tx_outs: [
    # { value: 1,
    #   address: ""},
    # { value: 2
    #   address: ""}
    # ],
    # "locktime": 0,
    # }

    vin = []
    for utxo_hash in request_data["utxos"]:
        tx_hash, tx_output_n = utxo_hash[: 64], utxo_hash[64: ]
        utxo_data = utxo_db.find_utxo(_address = current_user.address, _tx_hash = tx_hash, _tx_output_n = tx_output_n)

        if not utxo_data:
            response = {
                "message": "utxos you have requested do not exist"
            }
            return jsonify(response), 400

    
        transaction = blockchain.get_tx(_block_height = utxo_data["block_height"], _tx_hash = utxo_data["tx_hash"]) 
        signature = Wallet.generate_signature(_private_key = current_user.private_key, 
                                              _data = transaction.to_json(), 
                                              _public_key = current_user.public_key)

        tx_in = TransactionInput(_tx_hash = utxo_data["tx_hash"], 
                                 _tx_output_n = utxo_data["tx_output_n"], 
                                 _signature = signature,
                                 _public_key = current_user.public_key)
        vin.append(tx_in)
        # txin = create_transaction_input(current_user.private_key, 
        #                                 current_user.public_key, 
        #                                 previous_transaction = transaction, 
        #                                 tx_hash = utxo["tx_hash"], 
        #                                 tx_output_n = utxo["tx_output_n"])
        # txin_list.append(txin)

    vout = []
    for tx_out in request_data["tx_outs"]:
        vout.append(TransactionOutput(_value = tx_out["value"],
                                            _address = tx_out["address"]))

    transaction = Transaction(_vin = vin, 
                              _vout = vout,
                              _version = 0,
                              _locktime = request_data["locktime"])

    requests.post("/add-transaction", json = {"transaction": transaction.to_dict()})

@network.route("/add-transaction", methods=["POST"])
def add_transaction():
    request_data = request.get_json()

    if not request_data:
        response = {
            'message': 'No data attached.'
        }
        return jsonify(response), 400
    if request_data.get("transaction", None) is None :
        response = {
            'message': 'No transaction data found.'
        }
        return jsonify(response), 400

    transaction = request_data["transaction"]
    address = request_data["address"]

    verification = Verification(transaction)
    if verification.in_mempool():
        response = {
            "message": "The requested transaction has already been in process"
        }
        return jsonify(response), 400

    elif not verification.valid_funds(current_user.address):
        response = {
            "message": "The fund is not enough"
        }
        return jsonify(response), 400

    utxos = []
    for txin in transaction["vin"]:
        utxos.append(utxo_db.find_utxo(_address = address, 
                                       _tx_hash = txin["tx_hash"], 
                                       _tx_output_n = txin["tx_output_n"]))

    if not verification.success_unlock(_utxos = utxos):
        response = {
            "message": "The utxos are not valid"
        }
        return jsonify(response), 400

    elif mempool.add_tx(transaction["tx_hash"], transaction):
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

    mempool.add_tx(_tx_hash = transaction["tx_hash"], _transaction = transaction)
    
   
@network.route("/broadcast-transaction", methods=["POST"])
def broadcast_transaction():
    request_data = request.get_json()
    
    requests.post("/add-transaction", json = {"transaction": transaction.to_dict()})

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




