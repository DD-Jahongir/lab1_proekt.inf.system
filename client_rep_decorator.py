from client_rep_adapter import ClientRepositoryBase
from client import Client

class ClientRepositoryDecorator(ClientRepositoryBase):
    def __init__(self, wrapped_repo: ClientRepositoryBase):
        self._wrapped = wrapped_repo

    def get_by_id(self, client_id: int) -> Client:
        return self._wrapped.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> list:
        return self._wrapped.get_k_n_short_list(k, n)

    def add(self, client: Client):
        self._wrapped.add(client)

    def update(self, client_id: int, new_client: Client):
        self._wrapped.update(client_id, new_client)

    def delete(self, client_id: int):
        self._wrapped.delete(client_id)

    def get_count(self) -> int:
        return self._wrapped.get_count()


class ClientRepositoryLogger(ClientRepositoryDecorator):
    def add(self, client: Client):
        print(f"[ЛОГ] Начинается добавление клиента: {client.last_name} {client.first_name}")
        super().add(client)
        print("[ЛОГ] Клиент успешно добавлен в систему.")

    def delete(self, client_id: int):
        print(f"[ЛОГ] Внимание: попытка удаления клиента с ID={client_id}")
        super().delete(client_id)
        print(f"[ЛОГ] Клиент с ID={client_id} безвозвратно удален.")

    def update(self, client_id: int, new_client: Client):
        print(f"[ЛОГ] Обновление данных клиента ID={client_id}")
        super().update(client_id, new_client)
        print("[ЛОГ] Данные успешно обновлены.")