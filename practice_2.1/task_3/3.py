import csv

data = [
    ["Название", "Цена", "Количество"],
    ["Яблоки", 100, 50],
    ["Бананы", 80, 30],
    ["Молоко", 120, 20],
    ["Хлеб", 40, 100]
]

with open('../resource/products.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)


def read_products():
    with open('../resource/products.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def save_products(products):
    with open('../resource/products.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Название", "Цена", "Количество"])
        writer.writeheader()
        writer.writerows(products)


while True:
    print("\n" + "=" * 40)
    print("1 - Показать товары")
    print("2 - Добавить товар")
    print("3 - Поиск товара")
    print("4 - Общая стоимость")
    print("5 - Сохранить отсортированные по цене")
    print("6 - Выход")

    choice = input("Выберите действие: ")

    if choice == '1':
        products = read_products()
        for p in products:
            print(f"{p['Название']}: {p['Цена']} руб, {p['Количество']} шт")

    elif choice == '2':
        name = input("Название: ")
        price = int(input("Цена: "))
        qty = int(input("Количество: "))
        products = read_products()
        products.append({"Название": name, "Цена": price, "Количество": qty})
        save_products(products)
        print("Товар добавлен!")

    elif choice == '3':
        search = input("Введите название: ")
        products = read_products()
        found = [p for p in products if search.lower() in p['Название'].lower()]
        if found:
            for p in found:
                print(f"{p['Название']} - {p['Цена']} руб, {p['Количество']} шт")
        else:
            print("Не найдено")

    elif choice == '4':
        products = read_products()
        total = sum(int(p['Цена']) * int(p['Количество']) for p in products)
        print(f"Общая стоимость всех товаров: {total} руб")

    elif choice == '5':
        products = read_products()
        sorted_products = sorted(products, key=lambda x: int(x['Цена']))
        with open('sorted_products.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Название", "Цена", "Количество"])
            writer.writeheader()
            writer.writerows(sorted_products)
        print("Сохранено в sorted_products.csv")

    elif choice == '6':
        break