from src.block.chain import Blockchain
from .transaction import Transaction
from .transaction_in import TransactionInput
from .transaction_out import TransactionOutput
from src.block.memory_pool import Mempool
from src.block.utxo_pool import UtxoDB
from src.block.chain import Blockchain

mempool = Mempool("localhost", 6379)
utxo_db = UtxoDB('localhost', 27017)
utxo_db.connect_db("utxo")
utxo_db.connect_collection("utxo")
chain = Blockchain()
from src.utils.script import Script

class Verification:
    def __init__(self, _address, _transaction:dict):
        # _address is sender's address
        self.address = _address
        self.tx = _transaction
        self.vin = _transaction["vin"]
        self.vout = _transaction["vout"]
        self.utxos = []

    def in_mempool(self):
        if mempool.get_tx(_tx_hash = self.tx["tx_hash"]) != -1:
            return True 

        elif self.__in_mempool_vin(_address = self.address):
            return True
        
        elif self.__in_mempool_vout():
            return True 

        else:
            return False 

    def __in_mempool_vin(self):  
        # 
        return any([mempool.tx_in_exists(_address = self.address, 
                                         _tx_hash = tx_in["tx_hash"], 
                                         _tx_output_n = tx_in["tx_output_n"]) for tx_in in self.vin[:]])
    
    def __in_mempool_vout(self):
        # prevent using utxo in the memory pool
        # transaction inputs must not be transaction outputs in the mempool
        return any([mempool.tx_out_exists(_tx_hash = tx_in["tx_hash"], 
                                          _tx_output_n = tx_in["tx_output_n"]) for tx_in in self.vin[:]])

    # def in_utxos(self, _address:str): 
    #     for txin in self.vin[:]:
    #         try:
    #             data = utxo_db.find_utxo(_address = _address, 
    #                                     _tx_hash = txin["tx_hash"], 
    #                                     _tx_output_n = txin["tx_output_n"])
    #             if not data:
    #                 return False 
    #         except Exception as e:
    #             print(f"Error: {e}")    
    #             return False 
    #     else:
    #         return True

    def valid_funds(self):
        total_input = 0
        total_output = 0
        for tx_in in self.vin[:]:
            utxo = utxo_db.find_utxo(_address = self.address, 
                                     _tx_hash = tx_in["tx_hash"], 
                                     _tx_output_n = tx_in["tx_output_n"])
            total_input += utxo["value"]

        for tx_out in self.vout[:]:
            total_output += tx_out["value"]

        if total_input < total_output:
            return False 

        return True

    def success_unlock(self, _utxos):
        for txin, utxo in zip(self.vin, _utxos):
            tx_hash, tx_output_n, block_height = utxo["tx_hash"], utxo["tx_output_n"], utxo["block_height"]
            tx = chain.get_tx(_block_height = block_height, _tx_hash = tx_hash)
            script = txin["script_sig"] + "\t" + utxo["script_key"]
            unlocker = Script(tx)
            success = unlocker.run(script)
            if not success:
                return False 
        else:
            return True 
                

    




    
        

