import time, requests, json
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.utils.constants import DIFFICULTY, MINING_REWARD
from src.transaction.transaction import Transaction
from src.transaction.transaction_in import TransactionInput
from src.transaction.transaction_out import TransactionOutput
from src.block.block import BlockHead, Block
from src.utils.proof_of_work import ProofOfWork
from src.block.memory_pool  import add_tx, delete_all, get_all
from src.block.blockchain import Blockchain
from src.wallet.wallet import Wallet
from src.utils.utils import MerkleTree
from src.block.utxo_pool import get_utxo, get_utxos
from src.wallet.wallet import Wallet
from src.network.node_db import get_all as node_get_all, get_one as node_get_one, save_one as node_save_one
from src.utils.script import Script

network = Blueprint("network", __name__)
VERSION = 0

if current_user.is_authenticated():
    global blockchain 
    blockchain = Blockchain.load_from_db()

def verify_transaction(transaction:Transaction, address:str):
    if transaction.in_mempool() or not transaction.valid_funds():
        return False 

    for tx_in in transaction.vin:
        utxo = get_utxo(address = address, 
                        tx_hash = tx_in.tx_hash, 
                        tx_output_n = tx_in.tx_output_n)
        
        tx = blockchain.get_tx(block_height = utxo["block_height"], tx_hash = utxo["tx_hash"])
        unlocker = Script(tx.to_json())
        script = f"{tx_in.script_sig}\t{utxo['script_key']}"
        success = unlocker.run(script)
        if not success:
            return True

def broadcast(transaction:Transaction, address:str):
    data = {"transaction": transaction.to_dict(),
            "address": address}
    for hostname, address in node_get_all():
        try:
            response = requests.post(f"http://{hostname}/broadcast-transaction", json = data)
            if response.status_code == 400 or response.status_code == 500:
                print("broadcasing transaction error")
                return False 
        except requests.exceptions.ConnectionError:
            return False 
    return True

@network.route("/blockchain", methods=["GET"])
@login_required
def get_blockchain():
    try:
        response = {
            "chain": blockchain.to_dict(),
            "height": blockchain.height,
            "last_block_hash": blockchain.last_block.block_hash
        }
        return jsonify(response), 200
    except Exception as e:
        print(f"Error: {e}")
        response = {
            "message": "Blockchain not found."
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

@network.route("/transaction", methods=["POST"])
@login_required
def create_transaction():
    request_data  = request.get_json()
    if not request_data:
        response = {
            "message": "Data not found."
        }
        return jsonify(response), 400

    vin = []
    for utxo_hash in request_data["utxos"]:
        tx_hash, tx_output_n = utxo_hash[: 64], utxo_hash[64: ]
        utxo_data = get_utxo(address = current_user.address, 
                            tx_hash = tx_hash, 
                            tx_output_n = tx_output_n)

        if utxo_data is None:
            response = {
                "message": "utxo you requested not exists"
            }
            return jsonify(response), 400

        transaction = blockchain.get_tx(block_height = utxo_data["block_height"], 
                                        tx_hash = tx_hash) 

        signature = Wallet.generate_signature(private_key = current_user.private_key, 
                                            data = transaction.to_json(), 
                                            public_key = current_user.public_key) 

        tx_in = TransactionInput(tx_hash = tx_hash, 
                                tx_output_n = tx_output_n, 
                                signature = signature,
                                public_key = current_user.public_key)
        vin.append(tx_in)

    vout = []
    for tx_out in request_data["tx_outs"]:
        vout.append(TransactionOutput(value = tx_out["value"],
                                    address = tx_out["address"]))

    transaction = Transaction(vin = vin, 
                            vout = vout,
                            version = VERSION,
                            locktime = request_data["locktime"])
        
    success = verify_transaction(transaction, current_user.address)
    if not success:
        response = {
                "message": "verifying the transaction failed"
            }
        return jsonify(response), 400

    success = add_tx(tx_hash = transaction["tx_hash"], transaction = transaction)
    if not success:
        response = {
                "message": "adding the transaction failed."
            }
        return jsonify(response), 400

    success = broadcast(transaction, current_user.address)
    if not success:
        response = {
                "message": "broadcasting the transaction failed."
            }
        return jsonify(response), 400

        
@network.route("/broadcast-transaction", methods=["POST"])
def broadcast_transaction():
    request_data = request.get_json()
    transaction = Transaction.load(**request_data["transaction"])
    address = request_data["address"]

    success = verify_transaction(transaction = transaction, address = address)
    if not success:
        response = {
                "message": "verifying the transaction failed"
            }
        return jsonify(response), 400

    success = add_tx(tx_hash = transaction["tx_hash"], transaction = transaction)
    if not success:
        response = {
                "message": "adding the transaction failed."
            }
        return jsonify(response), 400

    success = broadcast(transaction = transaction, address = current_user.address)
    if not success:
        response = {
                "message": "broadcasting the transaction failed."
            }
        return jsonify(response), 400

    

@network.route("/mine", methods=["POST"])
def mine():
    if blockchain.has_conflict:
        requests.post("/resolve-conflict")
        response = {
            'message': 'a request conflicts with differennt blockchain nodes'
        }
        return jsonify(response), 409

    tx_list = [Transaction(vin = [], vout = [TransactionOutput(MINING_REWARD, current_user.address)])]
    tx_list.extend([Transaction.load(json.loads(tx)) for tx in get_all()])
    last_block_hash = blockchain.last_block.head.block_hash
    tx_hash_list = [tx.tx_hash for tx in tx_list[1: ]]
    merkle_root_hash = MerkleTree.generate_merkle_root(tx_hash_list)
    timestamp = time.time()

    nonce = ProofOfWork.get_nonce(merkle_root_hash = merkle_root_hash, 
                                  previous_block_hash = last_block_hash,
                                  difficulty = DIFFICULTY, 
                                  timestamp = timestamp)

    block_head = BlockHead(version = 0, 
                           previous_block_hash = last_block_hash, 
                           merkle_root_hash = merkle_root_hash, 
                           difficulty = DIFFICULTY,
                           nonce = nonce,
                           timestamp = timestamp)

    block = Block(tx_list = tx_list, block_head = block_head)
    block_dict = block.to_dict()
    block_height = blockchain.height

    blockchain.add_block(block_dict)
    delete_all()

    for hostname, address in node_get_all:
        try:
            response = requests.post(f"http://{hostname}/broadcast-block", {"block": block_dict,
                                                                            "block_height": block_height})
            if response.status_code == 400 or response.status_code == 500:
                response = {
                    "message": "mining failed."
                }
                return jsonify(response), 400

            if response.status_code == 409:
                blockchain.has_conflicts = True
                response = {
                    "message": "blockchain conflicts with other nodes."
                }
                # return jsonify(response), 400
                print(response)
        except requests.exceptions.ConnectionError:
            continue
    return jsonify({"block": block.to_dict()}), 201

@network.route("/broadcast-block", methods=["POST"])
def broadcast_block():
    request_data = request.get_json()
    if not request_data:
        response = {
            'message': 'Data not found.'
        }
        return jsonify(response), 400

    elif not all(key in request_data for key in ["block", "block_height"]):
        response = {
            'message': 'Some data is missing.'
        }
        return jsonify(response), 400

    elif request_data['block']["block_head"]["previous_block_hash"] != blockchain.last_block.block_hash and\
        request_data["block_height"] <= blockchain.height: 
        response = {
            'message': "Blockchain conflicts with other nodes."
        }
        return jsonify(response), 409

    elif not blockchain.verify_chain():
        response = {
            'message': 'local blockchain is not valid.'
        }
        return jsonify(response), 400

    block = Block.load(request_data['block'])
    if  ProofOfWork.valid_nonce(merkle_root_hash = block.block_head.merkle_root_hash, 
                                previous_block_hash = block.block_head.prev_block_hash, 
                                difficulty = block.block_head.difficulty, 
                                timestamp = block.block_head.timestamp, 
                                nonce = block.block_head.nonce):
        blockchain.add_block(block)
        response = {
            "message": "Adding the block success"
        }
        return jsonify(response), 201
    

@network.route("/resolve-conflict", methods=["POST"])
def resolve_conflict():
    for hostname, address in node_get_all():
        try:
            response = requests.get(f"http://{hostname}/blockchain")
            if response.status_code == 400 or response.status_code == 500:
                return False 
        except requests.exceptions.ConnectionError:
            return False 

    if blockchain.height >= response["height"]:
        if blockchain.last_block.block_hash == response["block_hash"]:
            chain = response["chain"]
            len(chain)
            chain = chain.load(chain)
            return True


@network.route("/node", methods = ["GET"])
@network.route("/")
def node():
    nodes = node_get_all()
    return jsonify({"nodes": nodes}), 200

@network.route("/advatise-node", methods=["POST"])
@login_required
def advatise_node():
    request_data = request.get_json()
    if not request_data:
        response = {
            "message": "data not found"
        }
        return jsonify(response), 500

    elif "node" not in request_data:
        response = {
            "message": "node not found in the request"
        }
        return jsonify(response), 400
    
    elif node_get_one(request_data["node"]):
        response = {
            "message": "The node is already in the list."
        }
        return jsonify(response), 400
    
    node_save_one(hostname = request_data["node"]["hostname"], 
                  address = request_data["node"]["address"])
                  
    for hostname, address in node_get_all():
        data = {
            "hostname": hostname,
            "address": current_user.address
        }
        response = requests.post(f"http://{hostname}/advatise-node", json = data)



@network.route("/balance", methods=["GET"])
@login_required
def balance():
    try:
        utxos = get_utxos(address = current_user.address)
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




