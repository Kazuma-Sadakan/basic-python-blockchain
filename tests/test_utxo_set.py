from charset_normalizer import utils
from src.block.utxo_pool import UtxoDB
import unittest

class TestUtxoDB(unittest.TestCase):
    def setUp(self):
        self.db = UtxoDB('localhost', 27017)
        self.db.connect_db("utxo")
        self.db.connect_collection("utxo")

    def test_save(self):
        vout = [{"tx_hash": "111123dde201bc37db7dc57e0cb6243a875f3d0c799664d0a311c83633d2dbaf",
                'value': 1, 
                'script_pubkey': {'hex': 'OP_DUP\tOP_HASH160\t9995e3f2804e6ff8415ae84675ce9a1ad2d346a7\tOP_EQUALVERIFY\tOP_CHECKSIG'}, 
                "tx_output_n": 0,
                'address': 'mZXj8oBOb/hBWuhGdc6aGtLTRqc=',
                }, 
                {"tx_hash": "72b950d2a37ffaf7b595a84acd976875d84e82c00bfa47ff50aea0e827f5b8c4",
                'value': 2, 
                'script_pubkey': {'hex': 'OP_DUP\tOP_HASH160\t6ca91ccffb4a7fbbd0881434f782af6e421bb86f\tOP_EQUALVERIFY\tOP_CHECKSIG'}, 
                "tx_output_n": 0,
                'address': 'bKkcz/tKf7vQiBQ094KvbkIbuG8=',
                }]
        self.db.save_many('KvWgv2g+KIr36c0FLyhSHD5K7+o=', vout)

    def test_get_tx_hashes(self):
        print("[*] test get tx_hashes")
        for tx in self.db:
            print(tx)

    def test_get_item(self):
        print("[*] test get item")
        for key, unspent_outputs in self.db.items:
            print(key, "<*>", unspent_outputs)

    def test_find_utxo(self):
        print("[*] test find utxo")
        print(self.db.find_utxo("KvWgv2g+KIr36c0FLyhSHD5K7+o=", "111123dde201bc37db7dc57e0cb6243a875f3d0c799664d0a311c83633d2dbaf", 0))

    def test_find_utxos(self):
        print("[*] test get utxos")
        print(self.db.get_utxos('KvWgv2g+KIr36c0FLyhSHD5K7+o='))