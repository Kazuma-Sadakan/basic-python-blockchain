import json

"""
TransactionInput.to_json()

{"tx_hash": 13, 
"tx_output_n": 0, 
"script_sig": "<signature>\t<public_key>"  
}

"""

class TransactionInput:
    def __init__(self, 
                _tx_hash:str, 
                _tx_output_n:int,
                _signature:str = "",
                _public_key:str = ""):

        self.tx_hash = _tx_hash
        self.tx_output_n = _tx_output_n
        self.script_sig = "{}\t{}".format(_signature, _public_key) if all([_signature, _public_key]) else ""

    def __hash__(self):
        return hash((self.tx_hash, self.tx_output_n))

    def __eq__(self, other):
        return isinstance(other, TransactionInput) and \
               (self.tx_hash == other.tx_hash) and \
               (self.tx_output_n == other.tx_output_n)

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

tx = TransactionInput("123", 3)
print(vars(tx))