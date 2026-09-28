import json
import re

class ClientShort:
    def __init__(self, last_name: str, initials: str, phone_number: str):
        self.last_name = last_name
        self.initials = initials
        self.phone_number = phone_number

    def __str__(self) -> str:
        return f"{self.last_name} {self.initials}, Тел: {self.phone_number}"


class Client:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            data_string = args[0].strip()
            
            if data_string.startswith("{"):
                try:
                    data = json.loads(data_string)
                    self.client_id = data["client_id"]
                    self.last_name = data["last_name"]
                    self.first_name = data["first_name"]
                    self.passport_data = data["passport_data"]
                    self.phone_number = data["phone_number"]
                except KeyError as e:
                    raise ValueError(f"В JSON отсутствует поле: {e}")
                except json.JSONDecodeError:
                    raise ValueError("Передана некорректная JSON-строка.")
            
            else:
                normalized_string = data_string.replace(".", ",").replace(";", ",")
                parts = normalized_string.split(",")
                if len(parts) != 5:
                    raise ValueError("Строка должна содержать ровно 5 элементов.")
                
                self.client_id = int(parts[0].strip())
                self.last_name = parts[1].strip()
                self.first_name = parts[2].strip()
                self.passport_data = parts[3].strip()
                self.phone_number = parts[4].strip()
        
        elif len(args) == 5:
            self.client_id = args[0]
            self.last_name = args[1]
            self.first_name = args[2]
            self.passport_data = args[3]
            self.phone_number = args[4]
        
        else:
            raise ValueError("Неверное количество аргументов. Ожидается либо 1 строка, либо 5 параметров.")

    @staticmethod
    def _validate_string(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Поле '{field_name}' не может быть пустым.")
        
        value = value.strip()
        if not re.fullmatch(r"[А-Яа-яЁёA-Za-z\-\s]+", value):
            raise ValueError(f"Поле '{field_name}' содержит недопустимые символы (ожидаются только буквы).")
        
        return value.title()

    @staticmethod
    def _validate_passport(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Паспортные данные не могут быть пустыми.")
        
        value = value.strip()
        if not re.fullmatch(r"\d{4}\s\d{6}", value):
            raise ValueError("Паспорт должен быть в формате 'XXXX XXXXXX' (серия и номер через пробел).")
        
        return value

    @staticmethod
    def _validate_phone(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Телефон должен передаваться как строка.")
        
        cleaned = re.sub(r"[\s\-\(\)\+]", "", value)
        
        if not re.fullmatch(r"(7|8)?\d{10}", cleaned):
            raise ValueError(f"Некорректный формат телефона: {value}")
        
        return cleaned[-10:]

    @staticmethod
    def _validate_client_id(value: int) -> int:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID клиента должен быть положительным целым числом.")
        return value
    
    @property
    def client_id(self) -> int:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: int):
        self.__client_id = self._validate_client_id(value)

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        self.__last_name = self._validate_string(value, "Фамилия")

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        self.__first_name = self._validate_string(value, "Имя")

    @property
    def passport_data(self) -> str:
        return self.__passport_data

    @passport_data.setter
    def passport_data(self, value: str):
        self.__passport_data = self._validate_passport(value)

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: str):
        self.__phone_number = self._validate_phone(value)

    def __str__(self) -> str:
        return (f"Клиент #{self.client_id}: {self.last_name} {self.first_name}, "
                f"Паспорт: {self.passport_data}, Тел: {self.phone_number}")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Client):
            return False
        return self.passport_data == other.passport_data


class ClientMapper:
    @staticmethod
    def short_version(client) -> ClientShort:
            return ClientShort(client.last_name, f"{client.first_name[0]}.", client.phone_number)

if __name__ == "__main__":
    client1 = Client(1, "Иванов", "Иван", "1234 567890", "(999) 123-45-67")
    print("Стандартное создание:", client1)
    
    json_data = '{"client_id": 3, "last_name": "Попова", "first_name": "Анна", "passport_data": "5555 666666", "phone_number": "9223334455"}'
    client_json = Client(json_data)
    print("Создание из JSON:", client_json)
    
    csv_data = "4, Кузнецов, Дмитрий, 9999 000000, 9556667788"
    client_csv = Client(csv_data)
    print("Создание из строки:", client_csv)
    




    client3 = Client(6, "ASSD", "asdsf", "1564 984695", "(996) 123-45-67")
    full_clients = [client1, client_json, client_csv]
    clientsShorts = [ClientMapper.short_version(client1), ClientMapper.short_version(client_json), ClientMapper.short_version(client_csv)]

    for i in clientsShorts:
        print(i)
