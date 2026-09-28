from client import Client, ClientMapper

class ClientRepositoryBase:
    def __init__(self):
        self.clients = []

    def read_from_file(self):
        raise NotImplementedError("Метод должен быть реализован в классе-наследнике")

    def write_to_file(self):
        raise NotImplementedError("Метод должен быть реализован в классе-наследнике")

    def get_by_id(self, client_id: int) -> Client:
        for c in self.clients:
            if c.client_id == client_id:
                return c
        raise ValueError(f"Клиент с ID {client_id} не найден.")

    def get_k_n_short_list(self, k: int, n: int) -> list:
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
                new_client.client_id = client_id
                self.clients[i] = new_client
                return
        raise ValueError(f"Клиент с ID {client_id} не найден.")

    def delete(self, client_id: int):
        self.clients = [c for c in self.clients if c.client_id != client_id]

    def get_count(self) -> int:
        return len(self.clients)