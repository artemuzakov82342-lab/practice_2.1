import requests
import json

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = "save.json"


def get_data():
    return requests.get(URL).json()


def show_all():
    data = get_data()["Valute"]
    for code, val in data.items():
        print(f"{code}: {val['Value']}")


def show_one(code):
    data = get_data()["Valute"]
    if code in data:
        print(data[code])
    else:
        print("Валюта не найдена")


def load_groups():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_groups(groups):
    with open(SAVE_FILE, "w") as f:
        json.dump(groups, f, indent=4)


def add_group(name):
    groups = load_groups()
    groups[name] = []
    save_groups(groups)


def add_currency(group, code):
    groups = load_groups()
    if group in groups:
        groups[group].append(code)
        save_groups(groups)


def show_groups():
    groups = load_groups()
    print(groups)


if __name__ == "__main__":
    while True:
        print("\n1 - Все валюты")
        print("2 - Одна валюта")
        print("3 - Создать группу")
        print("4 - Добавить валюту в группу")
        print("5 - Показать группы")
        print("0 - Выход")

        choice = input("Выбор: ")

        if choice == "1":
            show_all()
        elif choice == "2":
            code = input("Код валюты: ").upper()
            show_one(code)
        elif choice == "3":
            name = input("Название группы: ")
            add_group(name)
        elif choice == "4":
            group = input("Группа: ")
            code = input("Код валюты: ").upper()
            add_currency(group, code)
        elif choice == "5":
            show_groups()
        elif choice == "0":
            break