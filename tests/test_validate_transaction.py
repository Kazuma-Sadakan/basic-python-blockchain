import unittest
import time 

from src.transaction.verification import Validation
from src.transaction.transaction import Transaction, TransactionInput, TransactionOutput
from src.wallet.wallet import Wallet
from src.utils.utils import create_transaction_input

from src.block.memory_pool import Mempool
mempool = Mempool("localhost", 6379)

class TestValidation(unittest.TestCase):
    def setUp(self):
        self.wallet1 = Wallet("123")
        self.wallet2 = Wallet("234")

        coinbase_transaction = Transaction(vin=[], vout=[TransactionOutput(3, self.wallet1.address)])
        tx_hash = coinbase_transaction.tx_hash
        txin_1 = create_transaction_input(self.wallet1.private_key, self.wallet1.public_key, coinbase_transaction, tx_hash, 0)
        txout_1 = TransactionOutput(1, self.wallet2.address)
        txout_2 = TransactionOutput(2, self.wallet1.address)
        self.tx = Transaction([txin_1], [txout_1, txout_2], 0, time.time())
        self.mempool = Mempool("localhost", 6379)
        self.mempool.set(self.tx.tx_hash, self.tx.to_json())
        self.validation = Validation(self.tx.to_dict())

    def test_in_mempool(self):
        print("[*] test in mempool")
        print(self.validation.in_mempool())
        print(self.tx.to_json())
        for tx in mempool.get_all():
            print(tx)
    

if __name__ == "__main__":
    unittest.main()