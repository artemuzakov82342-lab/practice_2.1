import json
import os

FILE_NAME = '../resource/library.json'

initial_books = [
    {"id": 1, "title": "Мастер и Маргарита", "author": "Булгаков", "year": 1967, "available": True},
    {"id": 2, "title": "Преступление и наказание", "author": "Достоевский", "year": 1866, "available": False}
]


def load_books():
    """Загружает книги из JSON файла"""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(initial_books, f, ensure_ascii=False, indent=2)
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_books(books):
    """Сохраняет книги в JSON файл"""
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def show_all_books():
    """Просмотр всех книг"""
    books = load_books()
    if not books:
        print("Библиотека пуста")
        return
    print("\n" + "=" * 60)
    print("ВСЕ КНИГИ:")
    for book in books:
        status = "Доступна" if book['available'] else "Выдана"
        print(f"ID:{book['id']} | {book['title']} | {book['author']} | {book['year']} | {status}")


def search_books():
    """Поиск по автору/названию"""
    query = input("Введите автора или название: ").lower()
    books = load_books()
    found = [b for b in books if query in b['title'].lower() or query in b['author'].lower()]

    if found:
        print("\nНайденные книги:")
        for book in found:
            status = "Доступна" if book['available'] else "Выдана"
            print(f"{book['title']} - {book['author']} ({book['year']}) - {status}")
    else:
        print("Ничего не найдено")


def add_book():
    """Добавление новой книги"""
    books = load_books()
    new_id = max([b['id'] for b in books], default=0) + 1

    title = input("Название: ")
    author = input("Автор: ")
    year = int(input("Год: "))

    books.append({
        "id": new_id,
        "title": title,
        "author": author,
        "year": year,
        "available": True
    })
    save_books(books)
    print(f"Книга '{title}' добавлена! ID: {new_id}")


def toggle_availability():
    """Изменение статуса доступности"""
    book_id = int(input("Введите ID книги: "))
    books = load_books()

    for book in books:
        if book['id'] == book_id:
            book['available'] = not book['available']
            status = "доступна" if book['available'] else "выдана"
            save_books(books)
            print(f"Статус изменен: книга теперь {status}")
            return
    print("Книга не найдена")


def delete_book():
    """Удаление книги по ID"""
    book_id = int(input("Введите ID книги для удаления: "))
    books = load_books()

    for i, book in enumerate(books):
        if book['id'] == book_id:
            deleted = books.pop(i)
            save_books(books)
            print(f"Книга '{deleted['title']}' удалена")
            return
    print("Книга не найдена")


def export_available():
    """Экспорт доступных книг в текстовый файл"""
    books = load_books()
    available = [b for b in books if b['available']]

    with open('../resource/available_books.txt', 'w', encoding='utf-8') as f:
        f.write("ДОСТУПНЫЕ КНИГИ:\n")
        f.write("=" * 50 + "\n")
        for book in available:
            f.write(f"{book['title']} - {book['author']} ({book['year']})\n")

    print(f"Экспортировано {len(available)} книг в available_books.txt")


def main():
    while True:
        print("\n" + "=" * 40)
        print("БИБЛИОТЕКА")
        print("1 - Просмотр всех книг")
        print("2 - Поиск книги")
        print("3 - Добавить книгу")
        print("4 - Изменить статус доступности")
        print("5 - Удалить книгу")
        print("6 - Экспорт доступных книг")
        print("7 - Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            show_all_books()
        elif choice == '2':
            search_books()
        elif choice == '3':
            add_book()
        elif choice == '4':
            toggle_availability()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            export_available()
        elif choice == '7':
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()