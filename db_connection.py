import psycopg2

class DBConnection:
    __instance = None

    def __new__(cls, db_config: dict = None):
        if cls.__instance is None:
            if db_config is None:
                raise ValueError("При первом создании подключения необходимо передать db_config.")
            
            cls.__instance = super().__new__(cls)
            
            cls.__instance.connection = psycopg2.connect(**db_config)
            cls.__instance.connection.autocommit = True
            
        return cls.__instance

    def get_connection(self):
        return self.connection