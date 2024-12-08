from tabulate import tabulate
import datetime

# Данные
users = [
    {"username": "admin", "password": "root", "role": "admin", "history": []},
    {"username": "user", "password": "test", "role": "user", "history": []}
]

locations = {
    "Россия": {
        "Москва": [
            {"id": 1, "name": "Server1", "cpu": "8 cores", "ram": "16GB", "disk": "1TB", "price": 1000,
             "status": "available"},
            {"id": 2, "name": "Server2", "cpu": "4 cores", "ram": "8GB", "disk": "500GB", "price": 500,
             "status": "available"},
        ],
        "Санкт-Петербург": [
            {"id": 3, "name": "Server3", "cpu": "16 cores", "ram": "32GB", "disk": "2TB", "price": 2000,
             "status": "available"},
        ],
    },
    "США": {
        "Нью-Йорк": [
            {"id": 4, "name": "Server4", "cpu": "8 cores", "ram": "16GB", "disk": "1TB", "price": 1500,
             "status": "unavailable"},
        ],
        "Сан-Франциско": [
            {"id": 5, "name": "Server5", "cpu": "4 cores", "ram": "8GB", "disk": "500GB", "price": 1200,
             "status": "available"},
        ],
    },
    "Израиль": {
        "Иерусалим": [
            {"id": 6, "name": "Server6", "cpu": "8 cores", "ram": "32GB", "disk": "1TB", "price": 1500,
             "status": "available"},
        ],
    },
    "Япония": {
        "Токио": [
            {"id": 7, "name": "Server7", "cpu": "8 cores", "ram": "32GB", "disk": "1TB", "price": 1500,
            "status": "available"},
        ],
    },
    "Швейцария": {
        "Берн": [
            {"id": 8, "name": "Server8", "cpu": "8 cores", "ram": "32GB", "disk": "1TB", "price": 1500,
            "status": "unavailable"},
        ],
    },
}


# Обработчик ошибок
def safe_input(prompt, cast_func=None, error_message="Неверный ввод. Попробуйте снова."):
    while True:
        try:
            user_input = input(prompt).strip()
            return cast_func(user_input) if cast_func else user_input
        except (ValueError, TypeError):
            print(error_message)


# Форматированный вывод
def format_table(data, headers):
    return tabulate(data, headers=headers, tablefmt="grid")


# Основные функции
def view_servers(sort_by=None, filters=None):
    print("\nДоступные серверы:")
    all_servers = [
        {"country": country, "city": city, **server}
        for country, cities in locations.items()
        for city, servers in cities.items()
        for server in servers
    ]

    if filters:
        for key, value in filters.items():
            all_servers = [s for s in all_servers if str(s.get(key)) == str(value)]

    if sort_by:
        all_servers = sorted(all_servers, key=lambda s: s.get(sort_by))

    headers = ["Страна", "Город", "ID", "Имя", "CPU", "RAM", "Диск", "Цена", "Статус"]
    table_data = [
        [s["country"], s["city"], s["id"], s["name"], s["cpu"], s["ram"], s["disk"], s["price"], s["status"]]
        for s in all_servers
    ]
    print(format_table(table_data, headers))


def rent_server(user):
    print("\nАренда сервера.")
    view_servers()
    server_id = safe_input("Введите ID сервера для аренды: ", int)
    
    # проверка на арендованые серваки
    rented_servers = {rental["server"] for rental in user["history"]}
    
    for country, cities in locations.items():
        for city, servers in cities.items():
            server = next((s for s in servers if s["id"] == server_id and s["status"] == "available"), None)
            if server:
                if server["name"] in rented_servers:
                    print(f"Вы уже арендовали сервер {server['name']}.")
                    return
                
                # + в историю
                server["status"] = "rented"
                user["history"].append({
                    "server": server["name"],
                    "country": country,
                    "city": city,
                    "date": str(datetime.date.today())
                })
                print(f"Сервер {server['name']} успешно арендован.")
                return
    
    print("Сервер недоступен для аренды или неверный ID.")



def view_history(user):
    print("\nИстория аренды:")
    if user["history"]:
        history_data = [
            (h["server"], h["country"], h["city"], h["date"]) for h in user["history"]
        ]
        print(format_table(history_data, ["Сервер", "Страна", "Город", "Дата"]))
    else:
        print("История пуста.")
def choose_locations_by_country_and_city():
    print(f'Доступные страны:')
    for country in locations:
        print(f'- {country}')
    country = safe_input('выберите страну: ')
    if country not in locations:
        print('Неверный выбор страны')
        return None, None
    else:
        print("Вы успешно выбрали: ", country)
        
    print(f'\nДоступные города в {country}: ')
    for city in locations[country]:
        print(f'- {city}')
    city = safe_input('Выберите город: ')
    if city not in locations[country]:
        print('Неверный выбор города')
        return None, None
    else:
        print("Вы успешно выбрали: ", city)
    return country, city
def view_locations_by_choose():
    country, city = choose_locations_by_country_and_city()
    if not country or not city:
        return

    servers = locations[country][city]
    if not servers:
        print("Серверы в выбранном местоположении отсутствуют.")
        return

    print(f'\nСервера в {city}, {country}: ')
    headers = ["ID", "Имя", "CPU", "RAM", "Диск", "Цена", "Статус"]
    table_data = [
        [server["id"], server["name"], server["cpu"], server["ram"], server["disk"], server["price"], server["status"]]
        for server in servers
    ]
    print(format_table(table_data, headers))

# Функции администратора
def add_server():
    print("\nДобавление нового сервера:")
    country = safe_input("Введите страну: ")
    if country not in locations:
        locations[country] = {}
    city = safe_input("Введите город: ")
    if city not in locations[country]:
        locations[country][city] = []
    
    # Создание уникальности серверов по имени
    existing_servers = {server["name"] for c in locations[country].values() for server in c}
    
    name = safe_input("Имя сервера: ")
    if name in existing_servers:
        print(f"Сервер с именем {name} уже существует!")
        return
    
    cpu = safe_input("Процессор: ")
    ram = safe_input("ОЗУ: ")
    disk = safe_input("Диск: ")
    price = safe_input("Цена: ", int)
    server_id = max((server["id"] for c in locations.values() for s in c.values() for server in s), default=0) + 1
    locations[country][city].append(
        {"id": server_id, "name": name, "cpu": cpu, "ram": ram, "disk": disk, "price": price, "status": "available"}
    )
    print(f"Сервер {name} добавлен успешно!")



def remove_server():
    print("\nУдаление сервера:")
    view_servers()
    server_id = safe_input("Введите ID сервера для удаления: ", int)
    for country, cities in locations.items():
        for city, servers in cities.items():
            server = next((s for s in servers if s["id"] == server_id), None)
            if server:
                servers.remove(server)
                print(f"Сервер {server['name']} успешно удален.")
                return
    print("Сервер с указанным ID не найден.")


def manage_users():
    print("\nУправление пользователями:")
    action = safe_input("Выберите действие (добавить (+)/удалить (-)): ").lower()
    if action == "добавить" or action == "+":
        username = safe_input("Введите логин: ")
        password = safe_input("Введите пароль: ")
        role = safe_input("Роль (user/admin): ").lower()
        users.append({"username": username, "password": password, "role": role, "history": []})
        print(f"Пользователь {username} добавлен.")
    elif action == "удалить" or action == "-":
        username = safe_input("Введите логин для удаления: ")
        user = next((u for u in users if u["username"] == username), None)
        if user:
            users.remove(user)
            print(f"Пользователь {username} удален.")
        else:
            print("Пользователь не найден.")

def admin_menu():
    while True:
        print("\nАдмин-панель:")
        print("1. Просмотреть серверы")
        print("2. Добавить сервер")
        print("3. Удалить сервер")
        print("4. Управление пользователями")
        print("5. Выйти")
        choice = safe_input("Ваш выбор: ", int)
        if choice == 1:
            view_servers()
        elif choice == 2:
            add_server()
        elif choice == 3:
            remove_server()
        elif choice == 4:
            manage_users()
        elif choice == 5:
            break
        else:
            print("Неверный выбор.")


# Меню пользователя
def user_menu(user):
    while True:
        print("\nМеню пользователя:")
        print("1. Просмотреть серверы")
        print("2. Арендовать сервер")
        print("3. История аренды")
        print("4. Выбор локации")
        print("5. Выйти")
        choice = safe_input("Ваш выбор: ", int)
        if choice == 1:
            view_servers()
        elif choice == 2:
            rent_server(user)
        elif choice == 3:
            view_history(user)
        elif choice == 4:
            view_locations_by_choose()
        elif choice == 5:
            break
        else:
            print("Неверный выбор.")


# Авторизация
def login():
    print("Добро пожаловать!")
    username = input("Логин: ")
    password = input("Пароль: ")
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)
    if user:
        return user
    print("Неверные логин или пароль.")
    return None


def main():
    user = login()
    if user:
        if user["role"] == "admin":
            admin_menu()
        elif user["role"] == "user":
            user_menu(user)


if __name__ == "__main__":
    main()
