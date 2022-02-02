import unittest
import time 
import json
from .setup import wallet1_private_key, wallet2_private_key
from src.transaction.transaction import Transaction, TransactionInput, TransactionOutput
from src.wallet.wallet import Wallet
from src.block.memory_pool import add_tx, get_tx, get_all, tx_in_exists, tx_out_exists, add_tx, get_keys, delete_all
from src.block.utxo_pool import save_one
class TestMempool(unittest.TestCase):
    def setUp(self):
        self.wallet1 = Wallet(wallet_id = "123", private_key = wallet1_private_key)
        self.wallet2 = Wallet(wallet_id = "234", private_key = wallet2_private_key)
        coinbase_transaction = Transaction(vin=[], vout=[TransactionOutput(3, self.wallet1.address)], version=0, locktime=0)
        tx_hash = coinbase_transaction.tx_hash
        signature = Wallet.generate_signature(private_key = self.wallet1.private_key, 
                                             data = coinbase_transaction.to_json(), 
                                             public_key = self.wallet1.public_key) 

        tx_in = TransactionInput(tx_hash = tx_hash, 
                                tx_output_n = 0, 
                                signature = signature,
                                public_key = self.wallet1.public_key)
        tx_out1 = TransactionOutput(1, self.wallet2.address)
        tx_out2 = TransactionOutput(2, self.wallet1.address)
        self.tx = Transaction([tx_in], [tx_out1, tx_out2], 0, time.time())


        ###### utxo ######
        # {"tx_hash": "72b950d2a37ffaf7b595a84acd976875d84e82c00bfa47ff50aea0e827f5b8c4",
        # 'value': 2, 
        # 'script_pubkey': {'hex': 'OP_DUP\tOP_HASH160\t6ca91ccffb4a7fbbd0881434f782af6e421bb86f\tOP_EQUALVERIFY\tOP_CHECKSIG'}, 
        # "tx_output_n": 0,
        # "block_height": 1,
        # 'address': 'bKkcz/tKf7vQiBQ094KvbkIbuG8=',
        # }
        # print("####", vars(tx_out1))
        

    def test_save(self):
        delete_all
        add_tx(self.tx.tx_hash, self.tx.to_json())
        for i, utxo in enumerate(self.tx.vout):
            utxo_data = {
                "tx_hash": self.tx.tx_hash,
                **utxo.to_dict(),
                "tx_output_n": i,
                "block_height": 1,
                "address": utxo.address
            }
            save_one(utxo.address, utxo_data)

    def test_get_keys(self):
        for key in get_keys():
            print(key)

    def test_get(self):
        print("[*] test_get")
        add_tx(self.tx.tx_hash, self.tx.to_json())
        tx = json.loads(get_tx(self.tx.tx_hash))
        self.assertEqual(tx["tx_hash"], self.tx.tx_hash)

    def test_get_all(self):
        print('[*] test get_all')
        for tx in get_all():
            print(tx["vout"])

    def test_find_one_in_vin(self):
        # check if the transaction exists in a vin of mempool
        self.assertFalse(tx_in_exists(self.wallet1.address, self.tx.tx_hash, 0))
    
    def test_find_one_in_vout(self):
        #check if the transaction exists in a vout of mempool
        self.assertTrue(tx_out_exists(self.tx.tx_hash, 1))

if __name__ == "__main__":
    unittest.main()