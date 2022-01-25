from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.Hash import RIPEMD160
import Crypto.Random
import binascii
import json
import os 
from enum import Enum

"""
ScriptPubKey : OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
ScriptSig : <Signature> <pubkey>

<signature> : Its a data which represents your digital signature done using the private key of your corresponding public key.
<pubkey> : Its a data representing your publickey.
<pubKeyHash> : hashed publick key with sha160

OP_DUP[operation]: Duplicates the top stack item.
OP_HASH160 [operation] : The input is hashed twice: first with SHA-256 and then with RIPEMD-160.
OP_EQUALVERIFY[operation] : Returns 1 if the inputs are exactly equal, 0 otherwise.
OP_CHECKSIG[operation] : Verifies digital Signature.    
###################################################################################################
script_pubkey = OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
script_sig = <sig> <pub_key>
script = <sig> <pub_key> OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG

<sig>
<sig> <pub_key> 
<sig> <pub_key> <pub_key>
<sig> <pub_key> <pubKeyHash> 
<sig> <pub_key> <pubKeyHash> <pubKeyHash> 
<sig> <pub_key> 
True
"""

# class Hash(Crypto.Hash):
#     def __init__(self):
#         super().__init__()

#     def sha256(self, data):
#         if type(data) != 'bytes':
#             data_ = 
#         hash = SHA256.new(binascii.unhexlify(last_el)).digest()

class Stack:
    def __init__(self):
        self.memory = []

    def push(self, el):
        self.memory.append(el)

    def pop(self):
        self.memory.pop()
    
    def empty(self):
        return not len(self.memory)

class Queue:
    def __init__(self):
        self.memory = []

    def enqueue(self, el):
        self.memory.append(el)

    def dequeue(self):
        self.memory.pop(0)

    def empty(self):
        return not len(self.memory)

class Command(Enum):
    OP_PUSH = "OP_PUSH"
    OP_DUP = "OP_DUP"
    OP_HASH160 = "OP_HASH160"
    OP_EQUALVERIFY = "OP_EQUALVERIFY"
    OP_CHECKSIG = "OP_CHECKSIG"

    def __init__(self, type, data = None):
        self.type = type 
        self.data = data 

class Script(Stack):
    def __init__(self, data):
        super().__init__()
        self.data  = data

        self.handlers = {
            "OP_DUP" : self._op_dup,
            "OP_HASH160" : self._op_hash160,
            "OP_EQUALVERIFY" : self._op_equalverify,
            "OP_CHECKSIG" : self._op_checksig,
        }

        self.q = Queue()

    def run(self, script):
        script_ = self._script_to_command(script)
        for s in script_:
            if s.starts_with("OP_"):
                # self.q.enqueue(Command(Command[s]))
                try:
                    self.handlers[s]()
                    return True
                except Exception as e:
                    return False 
            else:
                self.push(s)

        # while not self.empty():
        #     cmd = self.q.deque()
        #     self.handlers[cmd]()

    def _script_to_command(self, script):
        script_ = script.strip().split("\t")
        return script_

    def _op_dup(self, data=None):
        last_el = self.pop()
        self.push(last_el)
        self.push(last_el)

    def _op_hash160(self, data=None):
        last_el = self.pop()
        hashed_last_el = RIPEMD160.new(SHA256.new(binascii.unhexlify(last_el)).digest()).digest()
        self.push(hashed_last_el)

    def _op_equalverify(self, data=None):
        el = self.pop()
        assert el == self.pop()

    def _op_checksig(self, data=None):
        public_key = self.pop()
        signature  = self.pop()
        verifier = DSS.new(DSA.import_key(binascii.unhexlify(public_key)))
        hashed_data = SHA256.new(json.dumps(self.data))
        verifier.verify(hashed_data, binascii.unhexlify(signature))

# script = "OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG"
# s = Script()
