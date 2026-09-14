class Client:
    def __init__(self, client_id: int, last_name: str, first_name: str, passport_data: str, phone_number: str):
        self.client_id = client_id
        self.last_name = last_name
        self.first_name = first_name
        self.passport_data = passport_data
        self.phone_number = phone_number


    @staticmethod
    def _validate_client_id(value: int) -> int:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID клиента должен быть положительным целым числом.")
        return value

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