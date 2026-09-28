from client import Client
from client_rep_json import Client_rep_json
from client_rep_yaml import Client_rep_yaml
import os

def run_tests(repo, file_name):
    print(f"Тестирование:{repo.__class__.__name__}")

    if os.path.exists(file_name):
        os.remove(file_name)
    repo.clients = []

    print("1. Добавление новых клиентов...")
    repo.add(Client(1, "Яковлев", "Яков", "1111 222222", "9991112233"))
    repo.add(Client(1, "Иванов", "Иван", "3333 444444", "9995556677"))
    repo.add(Client(1, "Алексеев", "Алексей", "5555 666666", "8880001122"))
    
    print(f"2. Количество элементов в памяти: {repo.get_count()}")

    print("\n3. Сортировка по фамилии:")
    repo.sort_by_last_name()
    for c in repo.clients:
        print(f"   - {c.last_name} {c.first_name} (ID: {c.client_id})")

    print("\n4. Получение короткого списка (k=2, n=1, первая страница):")
    short_list = repo.get_k_n_short_list(k=2, n=1)
    for short_client in short_list:
        print(f"   - {short_client}")

    print("\n5. Получение клиента по ID=2:")
    client_to_update = repo.get_by_id(2)
    print(f"   - Найден: {client_to_update}")

    print("\n6. Обновление клиента с ID=2 (меняем имя на 'Петр'):")
    client_to_update.first_name = "Петр"
    repo.update(2, client_to_update)
    print(f"   - После обновления: {repo.get_by_id(2)}")

    print("\n7. Удаление клиента с ID=1:")
    repo.delete(1)
    print(f"   - Количество элементов после удаления: {repo.get_count()}")

    print(f"\n8. Сохранение данных в {file_name} и повторное чтение...")
    repo.write_to_file()
    
    repo.clients = [] 
    repo.read_from_file()
    print(f"   - Успешно прочитано элементов из файла: {repo.get_count()}")
    for c in repo.clients:
        print(f"   - {c}")


if __name__ == "__main__":
    # Тестируем JSON
    json_repo = Client_rep_json("test_data.json")
    run_tests(json_repo, "test_data.json")

    # Тестируем YAML
    yaml_repo = Client_rep_yaml("test_data.yaml")
    run_tests(yaml_repo, "test_data.yaml")