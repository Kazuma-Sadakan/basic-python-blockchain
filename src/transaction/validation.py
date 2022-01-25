from .transaction import Transaction
from .transaction_in import TransactionInput
from .transaction_out import TransactionOutput
from src.block.memory_pool import Mempool
from src.block.utxo_pool import UtxoDB

mempool = Mempool("localhost", 6379)
db = UtxoDB('localhost', 27017)
db.connect_db("utxo")
db.connect_collection("utxo")

from src.utils.script import Script

class Validation:
    def __init__(self, transaction):
        self.tx = transaction
        self.vin = transaction["vin"]
        self.vout = transaction["vout"]
        self.utxos = []

    def in_mempool(self):
        if mempool.get(self.tx["tx_hash"]) != -1:
            return True 

        elif self.__in_mempool_vin():
            return True
        
        elif self.__in_mempool_vout():
            return True 

        else:
            return False 

    def __in_mempool_vin(self):  
        return any([mempool.find_one_in_vin(txin["tx_hash"], txin["tx_output_n"]) for txin in self.vin])
    
    def __in_mempool_vout(self):
        return any([mempool.find_one_in_vout(txin["tx_hash"], txin["tx_output_n"]) for txin in self.vin])

    def in_utxos(self, address): 
        for txin in self.vin:
            try:
                data = db.find_utxo(address, txin["tx_hash"], txin["tx_output_n"])
                if not data:
                    return False 
            except Exception as e:
                print(f"Error: {e}")    
                return False 
        else:
            return True

    def collect_utxos(self, address):
        for txin in self.vin:
            self.utxos.append(db.find_utxo(address, txin["tx_hash"], txin["tx_output_n"]))

    def validate_funds(self, address):
        total_input = 0
        total_output = 0
        for txin in self.vin:
            data = db.find_utxo(address, txin["tx_hash"], txin["tx_output_n"])
            total_input += data["value"]

        for txout in self.vout:
            total_output += txout["value"]

        if total_input < total_output:
            return False 

        return True

    # def unlock_utxos(self, address):
    #     for txin, utxo in zip(self.vin, self.utxos):
    #         tx_hash, tx_output_n, block_height = utxo["tx_hash"], utxo["tx_output_n"], utxo["block_height"]
    #         tx = chain.get_transaction(block_height, tx_hash, tx_output_n)
    #         script = txin["script_sig"] + "\t" + utxo["script_key"]
    #         unlocker = Script(tx)
    #         if not unlocker.run(script):
    #             raise ValueError("transaction is invalid")

    




    
        

