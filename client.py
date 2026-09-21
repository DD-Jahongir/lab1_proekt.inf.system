import json

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
                parts = data_string.split(",")
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

    @property
    def short_version(self) -> ClientShort:
        initials = f"{self.first_name[0]}."
        return ClientShort(self.last_name, initials, self.phone_number)

    @staticmethod
    def _validate_string(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Поле '{field_name}' не может быть пустым.")
        return value.strip()

    @staticmethod
    def _validate_phone(value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Телефон должен передаваться как строка.")
        digits_only = ''.join(filter(str.isdigit, value))
        if len(digits_only) != 10:
            raise ValueError(f"Номер телефона должен состоять ровно из 10 цифр. Введено цифр: {len(digits_only)}")
        return digits_only

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
        self.__passport_data = self._validate_string(value, "Паспортные данные")

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


if __name__ == "__main__":
    client1 = Client(1, "Иванов", "Иван", "1234 567890", "(999) 123-45-67")
    print("Стандартное создание:", client1)
    
    json_data = '{"client_id": 3, "last_name": "Попова", "first_name": "Анна", "passport_data": "555 666", "phone_number": "9223334455"}'
    client_json = Client(json_data)
    print("Создание из JSON:", client_json)
    
    csv_data = "4, Кузнецов, Дмитрий, 999 000, 9556667788"
    client_csv = Client(csv_data)
    print("Создание из строки:", client_csv)
    
    print("\nКраткая версия Кузнецова:", client_csv.short_version)
    client_csv.first_name = "Алексей"
    print("Краткая версия Кузнецова после смены имени:", client_csv.short_version)