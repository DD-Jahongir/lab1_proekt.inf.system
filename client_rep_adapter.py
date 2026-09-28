from abc import ABC, abstractmethod
from client_rep_db import Client_rep_DB
from client import Client

class ClientRepositoryBase(ABC):
    """Абстрактный базовый класс, задающий общий интерфейс для всех репозиториев."""
    @abstractmethod
    def get_by_id(self, client_id: int) -> Client: pass
    
    @abstractmethod
    def get_k_n_short_list(self, k: int, n: int) -> list: pass
    
    @abstractmethod
    def add(self, client: Client): pass
    
    @abstractmethod
    def update(self, client_id: int, new_client: Client): pass
    
    @abstractmethod
    def delete(self, client_id: int): pass
    
    @abstractmethod
    def get_count(self) -> int: pass


class Client_rep_DB_Adapter(ClientRepositoryBase):
    def __init__(self, db_repository: Client_rep_DB):
        # Адаптер получает и "оборачивает" несовместимый объект (adaptee)
        self.adaptee = db_repository

    def get_by_id(self, client_id: int) -> Client:
        return self.adaptee.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> list:
        return self.adaptee.get_k_n_short_list(k, n)

    def add(self, client: Client):
        self.adaptee.add(client)

    def update(self, client_id: int, new_client: Client):
        self.adaptee.update(client_id, new_client)

    def delete(self, client_id: int):
        self.adaptee.delete(client_id)

    def get_count(self) -> int:
        return self.adaptee.get_count()