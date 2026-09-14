import json

class ClientShort:
    def __init__(self, last_name: str, initials: str, phone_number: str):
        self.last_name = last_name
        self.initials = initials
        self.phone_number = phone_number


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
        if len(digits_only) != 11:
            raise ValueError(f"Номер телефона должен состоять ровно из 10 цифр. Введено цифр: {len(digits_only)}")
        return digits_only


    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        self.__last_name = self._validate_string(value, "Фамилия")

    @property
    def initials(self) -> str:
        return self.__initials

    @initials.setter
    def initials(self, value: str):
        self.__initials = self._validate_string(value, "Инициалы")

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: str):
        self.__phone_number = self._validate_phone(value)


class Client(ClientShort):
    def __init__(self, client_id: int, last_name: str, first_name: str, passport_data: str, phone_number: str):
        checked_first_name = self._validate_string(first_name, "Имя")
        
        initials = f"{checked_first_name[0]}."
        super().__init__(last_name=last_name, initials=initials, phone_number=phone_number)

        self.client_id = client_id
        self.first_name = checked_first_name 
        self.passport_data = passport_data


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
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        self.__first_name = self._validate_string(value, "Имя")
        self.initials = f"{value[0]}."

    @property
    def passport_data(self) -> str:
        return self.__passport_data

    @passport_data.setter
    def passport_data(self, value: str):
        self.__passport_data = self._validate_string(value, "Паспортные данные")


    @classmethod
    def from_json(cls, json_string: str):
        """Создает объект Client из JSON-строки."""
        try:
            data = json.loads(json_string)
            return cls(
                client_id=data["client_id"],
                last_name=data["last_name"],
                first_name=data["first_name"],
                passport_data=data["passport_data"],
                phone_number=data["phone_number"]
            )
        except KeyError as e:
            raise ValueError(f"В JSON отсутствует необходимое поле: {e}")
        except json.JSONDecodeError:
            raise ValueError("Передана некорректная JSON-строка.")

    @classmethod
    def from_string(cls, data_string: str, delimiter: str = ","):
        """Создает объект Client из строки, разделенной запятыми."""
        parts = data_string.split(delimiter)
        if len(parts) != 5:
            raise ValueError("Строка должна содержать ровно 5 элементов.")
        
        return cls(
            client_id=int(parts[0].strip()),
            last_name=parts[1].strip(),
            first_name=parts[2].strip(),
            passport_data=parts[3].strip(),
            phone_number=parts[4].strip()
        )


    def __str__(self) -> str:
        return (f"Клиент #{self.client_id}: {self.last_name} {self.first_name}, "
                f"Паспорт: {self.passport_data}, Тел: {self.phone_number}")

    def get_short_info(self) -> str:
        return f"{self.last_name} {self.first_name[0]}., Тел: {self.phone_number}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Client):
            return False
        return self.passport_data == other.passport_data


if __name__ == "__main__":
    client1 = Client(1, "Иванов", "Иван", "1234 567890", "+7 (999) 123-45-67")
    client2 = Client(2, "Петров", "Иван", "1234 567890", "8-900-000-00-00") # Тот же паспорт
    
    print(client1)
    print("Кратко:", client1.get_short_info())
    
    print("Сравнение (одинаковый паспорт):", client1 == client2)

    print("Из JSON:", Client.from_json('{"client_id": 3, "last_name": "Попова", "first_name": "Анна", "passport_data": "555 666", "phone_number": "89223334455"}'))
    print("Из строки:", Client.from_string("4, Кузнецов, Дмитрий, 999 000, 89556667788"))

    try:
        Client(-1, "Сидоров", "", "123", "999")
    except ValueError as e:
        print("Ошибка валидации перехвачена:", e)