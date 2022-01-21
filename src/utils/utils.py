import hashlib
import binascii

class MerkleTree:
    def __init__(self):
        pass
    
    def hash(node):
        return hashlib.sha256(binascii.hexlify(str(node).encode("utf-8"))).hexdigest()

    @staticmethod
    def generate_merkle_root(nodes):
        nodes = MerkleTree.hash(nodes)
        def recursive(nodes):
            tree = []
            if len(nodes) % 2 != 0:
                nodes.append(nodes[-1])
            temp = []
            for node in nodes:
                temp.append(node)
                if len(temp) % 2 == 0:
                    tree.append(MerkleTree.hash(temp[0]+temp[1]))
                    temp = []
            if len(tree) == 1:
                return tree[0]
            else:
                return recursive(tree)
        return recursive(nodes)

    @staticmethod
    def verify_merkle_root(merkle_root, nodes):
        return merkle_root == MerkleTree.generate_merkle_root(nodes)

if __name__ == "__main__":
    data = [1,2,3,4,5]
    merkle_root = MerkleTree.generate_merkle_root(data)
    print(merkle_root)
    print(MerkleTree.verify_merkle_root(merkle_root, data))
