import binascii
import json
import os 
import base64

from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.Hash import RIPEMD160
import Crypto.Random

"""
    private_key => (ECDSA) => public_key =>
    (RIPEMD160(SHA256)) => raw_wallet_addres => 
    (BASE58CHECK) => wallet_address
"""

class Wallet:
    def __init__(self, wallet_id, private_key=None):
        if private_key:
            try:
                private_key = DSA.import_key(binascii.unhexlify(private_key))
            except Exception as e:
                print(f"Error: {e}")

        else:
            private_key = DSA.generate(1024, Crypto.Random.new().read)
        self.private_key = binascii.hexlify(private_key.exportKey(format='DER')).decode("utf-8")
        public_key = private_key.public_key()
        self.public_key = binascii.hexlify(public_key.exportKey(format='DER')).decode("utf-8")
        self.address = self.__generate_wallet_address(self.public_key)

        self.wallet_id = wallet_id

    @staticmethod
    def hash160(public_key):
        return RIPEMD160.new(SHA256.new(binascii.unhexlify(public_key)).digest()).hexdigest()

    @staticmethod
    def sha256(public_key):
        return SHA256.new(binascii.unhexlify(public_key)).hexdigest()

    @staticmethod
    def __generate_wallet_address(public_key):
        raw_address = Wallet.hash160(public_key)
        return base64.b64encode(binascii.unhexlify(raw_address)).decode('utf-8')

    @staticmethod
    def address_to_public_hashed_hash(address):
        return binascii.hexlify(base64.b64decode(address.encode("utf-8"))).decode("utf-8")

    @staticmethod
    def generate_signature(sender, data):
        key = DSA.import_key(binascii.unhexlify(sender))
        data_ = SHA256.new(data.encode('utf-8'))
        signer = DSS.new(key, mode = 'fips-186-3')
        return binascii.hexlify(signer.sign(data_)).decode("utf-8")

    @staticmethod
    def veriry_transaction(sender, signature, data):
        key = DSA.import_key(binascii.unhexlify(sender))
        data_ = SHA256.new(data.encode('utf-8'))
        verifier = DSS.new(key, mode='fips-186-3')
        return verifier.verify(data_, binascii.unhexlify(signature.encode('utf-8')))



if __name__ == "__main__":
    wallet = Wallet("123")
    print(wallet.private_key)
    address = wallet.address
    print(address)
    print(wallet.hash160(wallet.public_key))
    print(wallet.address_to_public_hashed_hash(address))
    sig = wallet.generate_signature(wallet.private_key, "hello world")
    print(wallet.veriry_transaction(wallet.private_key, sig, "hello world"))

    