import json
import os
from client import Client
from repository_base import ClientRepositoryBase

class Client_rep_json(ClientRepositoryBase):
    def __init__(self, file_path: str):
        super().__init__() # Вызов конструктора родителя (создаст self.clients = [])
        self.file_path = file_path
        self.read_from_file()

    def read_from_file(self):
        if not os.path.exists(self.file_path):
            self.clients = []
            return
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.clients = [Client(json.dumps(item)) for item in data]

    def write_to_file(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            data = [{
                "client_id": c.client_id, "last_name": c.last_name,
                "first_name": c.first_name, "passport_data": c.passport_data,
                "phone_number": c.phone_number
            } for c in self.clients]
            json.dump(data, f, ensure_ascii=False, indent=4)