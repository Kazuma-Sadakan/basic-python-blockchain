import unittest
import time 
import json
from src.transaction.transaction import Transaction, TransactionInput, TransactionOutput
from src.wallet.wallet import Wallet
from src.utils.utils import create_transaction_input
from src.block.memory_pool import Mempool

class TestMempool(unittest.TestCase):
    def setUp(self):
        self.wallet1 = Wallet("123")
        self.wallet2 = Wallet("234")

        coinbase_transaction = Transaction(_vin=[], _vout=[TransactionOutput(3, self.wallet1.address)])
        tx_hash = coinbase_transaction.tx_hash
        txin_1 = create_transaction_input(self.wallet1.private_key, self.wallet1.public_key, coinbase_transaction, tx_hash, 0)
        txout_1 = TransactionOutput(1, self.wallet2.address)
        txout_2 = TransactionOutput(2, self.wallet1.address)
        self.tx = Transaction([txin_1], [txout_1, txout_2], 0, time.time())
        self.mempool = Mempool("localhost", 6379)

    def test_get(self):
        print("[*] test_get")
        self.mempool.set(self.tx.tx_hash, self.tx.to_json())
        tx = json.loads(self.mempool.get(self.tx.tx_hash))
        self.assertEqual(tx["tx_hash"], self.tx.tx_hash)

    def test_get_all(self):
        print('[*] test get_all')
        for tx in self.mempool.get_all():
            print(json.loads(tx)["vout"])

    def test_get_item(self):
        print('[*] test get items')
        for key, tx in self.mempool.items:
            print(key, "<*>", json.loads(tx))

    def test_find_one_in_vin(self):
        self.assertTrue(self.mempool.find_one_in_vin('6c045ae94210cd8859af8fd8f4718e4025c47173395536edd89e3edcd0fa5f2d', 0))
    
    def test_find_one_in_vout(self):
        self.assertTrue(self.mempool.find_one_in_vout("bd92f6aff1a8610f08300e15c25b500edaf1f9451213b6f6d91ca47477c08bab", 1))

    def test_delete_all(self):
        for key in self.mempool.get_keys():
            self.mempool.remove(key)

if __name__ == "__main__":
    unittest.main()