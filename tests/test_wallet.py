import unittest
from src.wallet.wallet import Wallet 

class TestWallet(unittest.TestCase):

    def setUp(self):
        print("[*] setting up")
        self.wallet = Wallet("123")
        self.message = "hello world"
        self.signature = self.wallet.generate_signature(self.wallet.private_key, self.message, self.wallet.public_key)     

    def test_verify(self):
        print("[*] test verify_signature")
        self.assertFalse(self.wallet.veriry_signature(self.wallet.public_key, self.signature, self.message))

if __name__ == "__main__":
    unittest.main() 
    
    
    