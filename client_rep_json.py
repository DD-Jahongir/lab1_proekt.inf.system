import json
import os
from client import Client, ClientShort, ClientMapper  # Укажите правильное имя вашего файла с классами

class Client_rep_json:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.clients = []
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
                "client_id": c.client_id,
                "last_name": c.last_name,
                "first_name": c.first_name,
                "passport_data": c.passport_data,
                "phone_number": c.phone_number
            } for c in self.clients]
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_by_id(self, client_id: int) -> Client:
        for c in self.clients:
            if c.client_id == client_id:
                return c
        raise ValueError(f"Клиент с ID {client_id} не найден.")

    def get_k_n_short_list(self, k: int, n: int) -> list[ClientShort]:
        # k - количество записей, n - номер страницы (начиная с 1)
        start = (n - 1) * k
        end = start + k
        slice_clients = self.clients[start:end]
        return [ClientMapper.short_version(c) for c in slice_clients]

    def sort_by_last_name(self):
        self.clients.sort(key=lambda c: c.last_name)

    def add(self, client: Client):
        new_id = max([c.client_id for c in self.clients], default=0) + 1
        client.client_id = new_id
        self.clients.append(client)

    def update(self, client_id: int, new_client: Client):
        for i, c in enumerate(self.clients):
            if c.client_id == client_id:
                new_client.client_id = client_id  # Защита: сохраняем старый ID
                self.clients[i] = new_client
                return
        raise ValueError(f"Клиент с ID {client_id} не найден.")

    def delete(self, client_id: int):
        self.clients = [c for c in self.clients if c.client_id != client_id]

    def get_count(self) -> int:
        return len(self.clients)