import time 
from .setup import wallet1_private_key, wallet2_private_key
from src.transaction.transaction import Transaction, TransactionInput, TransactionOutput
from src.wallet.wallet import Wallet

import unittest

class TestTransaction(unittest.TestCase):
    def setUp(self): 
        self.wallet1 = Wallet(wallet_id="123", private_key = wallet1_private_key)
        self.wallet2 = Wallet(wallet_id="234", private_key = wallet2_private_key)

        coinbase_transaction = Transaction(_vin=[], _vout=[TransactionOutput(3, self.wallet1.address)], _version = 0 , _locktime = 0)
        tx_hash = coinbase_transaction.tx_hash
        signature = Wallet.generate_signature(_private_key = self.wallet1.private_key, 
                                              _data = coinbase_transaction, 
                                              _public_key = self.wallet1.public_key)

        txin_1 = TransactionInput(tx_hash, 0, signature, self.wallet2.public_key)
        txout_1 = TransactionOutput(1, self.wallet2.address)
        txout_2 = TransactionOutput(2, self.wallet1.address)
        self.tx = Transaction([txin_1], [txout_1, txout_2], _version = 0, _locktime = 0)

    def test_transaction(self):
        print("[*] ", self.tx.to_json())


if __name__ == "__main__":
    unittest.main()