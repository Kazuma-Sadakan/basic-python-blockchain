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
    (BASE58CHECK)or(BASE64CHECK) => wallet_address
"""

class Wallet:
    def __init__(self, private_key=None):
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

    def get(self):
        return {"private_key": self.private_key, "public_key": self.public_key, "address": self.address}

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
    def generate_signature(private_key, data, public_key):
        key = DSA.import_key(binascii.unhexlify(private_key))
        hash = SHA256.new(f"{data}\t{public_key}".encode('utf-8'))
        signer = DSS.new(key, mode = 'fips-186-3')
        return binascii.hexlify(signer.sign(hash)).decode("utf-8")

    @staticmethod
    def veriry_signature(public_key, signature, data):
        key = DSA.import_key(binascii.unhexlify(public_key))
        hash = SHA256.new(f"{data}\t{public_key}".encode('utf-8'))
        verifier = DSS.new(key, mode='fips-186-3')
        return verifier.verify(hash, binascii.unhexlify(signature.encode('utf-8')))



