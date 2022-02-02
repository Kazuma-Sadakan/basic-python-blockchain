from src.block.blockchain import init_blockchain
from src.block.memory_pool import delete_all as mempool_delete_all
from src.block.utxo_pool import delete_all as utxo_delete_all


success = mempool_delete_all()
if success:
    print("successed in initializing mempool")
else:
    print("failed in initializing mempool")

success = utxo_delete_all()
if success:
    print("successed in initializing utxo set")
else:
    print("failed in initializing utxo set")

success = init_blockchain()
if success:
    print("successed in initializing blockchain")
else:
    print("failed in initializing blockchain")