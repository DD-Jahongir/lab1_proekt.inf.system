import yaml
import os
from client import Client
from repository_base import ClientRepositoryBase

class Client_rep_yaml(ClientRepositoryBase):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.read_from_file()

    def read_from_file(self):
        if not os.path.exists(self.file_path):
            self.clients = []
            return
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or []
            self.clients = [
                Client(item["client_id"], item["last_name"], item["first_name"], 
                       item["passport_data"], item["phone_number"]) 
                for item in data
            ]

    def write_to_file(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            data = [{
                "client_id": c.client_id, "last_name": c.last_name,
                "first_name": c.first_name, "passport_data": c.passport_data,
                "phone_number": c.phone_number
            } for c in self.clients]
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)