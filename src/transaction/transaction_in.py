import json
"""
{"tx_hash": 13, 
"tx_output_n": 0, 
"script_sig": {
    "hex": "<signature>\t<public_key>"
    }
}
"""

class TransactionInput:
    def __init__(self, tx_hash, tx_output_n, signature="", pub_key=""):
        self.tx_hash = tx_hash
        self.tx_output_n = tx_output_n
        self.script_sig = f"{signature}\t{pub_key}" if not (signature == "" and pub_key == "") else ""

    def to_dict(self):
        return {
            "tx_hash": self.tx_hash,
            "tx_output_n": self.tx_output_n,
            "script_sig": {
                "hex": self.script_sig,
            }
        }

    def to_json(self):
        return json.dumps(self.to_dict())

