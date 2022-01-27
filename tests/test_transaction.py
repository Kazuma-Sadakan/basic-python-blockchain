import time 
from .setup import wallet1_private_key, wallet2_private_key
from src.transaction.transaction import Transaction, TransactionInput, TransactionOutput
from src.wallet.wallet import Wallet
from src.utils.utils import create_transaction_input

import unittest

class TestTransaction(unittest.TestCase):
    def setUp(self): 
        self.wallet1 = Wallet(wallet_id="123", private_key = wallet1_private_key)
        self.wallet2 = Wallet(wallet_id="234", private_key = wallet2_private_key)

        coinbase_transaction = Transaction(_vin=[], _vout=[TransactionOutput(3, self.wallet1.address)])
        tx_hash = coinbase_transaction.tx_hash
        txin_1 = create_transaction_input(self.wallet1.private_key, self.wallet1.public_key, coinbase_transaction, tx_hash, 0)
        txout_1 = TransactionOutput(1, self.wallet2.address)
        txout_2 = TransactionOutput(2, self.wallet1.address)
        self.tx = Transaction([txin_1], [txout_1, txout_2], 0, time.time())

    def test_transaction(self):
        print("[*] ", self.tx.to_json())


if __name__ == "__main__":
    unittest.main()