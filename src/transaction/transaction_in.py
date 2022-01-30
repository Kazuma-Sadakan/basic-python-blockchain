import json

class TransactionInput:
    def __init__(self, 
                tx_hash:str, 
                tx_output_n:int,
                signature:str = "",
                public_key:str = ""):

        self.tx_hash = tx_hash
        self.tx_output_n = tx_output_n
        self.script_sig = f"{signature}\t{public_key}" if all([signature, public_key]) else ""

    def __hash__(self):
        return hash((self.tx_hash, self.tx_output_n))

    def __eq__(self, other):
        return isinstance(other, TransactionInput) and \
               (self.tx_hash == other.tx_hash) and \
               (self.tx_output_n == other.tx_output_n)

    def to_json(self) -> str:
        return json.dumps(self.__dict__)