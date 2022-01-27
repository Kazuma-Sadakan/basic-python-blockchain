import os, json
from copy import deepcopy
import requests

class Node:
    def __init__(self, hostname, address):
        self.hostname = hostname
        self.address = address
        self.url = f"http:{hostname}"

    def __eq__(self, other):
        return self.hostname == other.hostname

    def get(self, endpoint):
        url = os.path.join(self.url, endpoint)
        request_data = requests.get(url)
        return request_data.json()
    
    def post(self, endpoint, data = None):
        url = os.path.join(self.url, endpoint)
        request_data = requests.post(url, json=data)
        return request_data

    def to_dict(self):
        return deepcopy({
            "hostname": self.hostname,
            "address": self.address
        })

    def to_json(self):
        return json.dumps(self.to_dict())

# class NodeDatabase:
#     def __init__(self, file_name):
#         self.file_path = os.path.join(BASE_DIR, file_name)
#         self.node_list = set()

#     def save(self):
#         with open(self.file_path, mode="w") as file:
#             file.write([node.to_json() for node in self.node_list])

#     def load(self):
#         with open(self.file_path, mode="w") as file:
#             nodes = file.read()
#         for node in nodes:
#             self.node_list.append(Node(**json.loads(node)))

#     def add(self, node):
#         self.node_list.append(node)
#         self.save()

    # def remove(self, node):
    #     self.node_list.remove(node)

