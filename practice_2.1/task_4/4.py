import math
from datetime import datetime
import os

LOG_FILE = '../resource/calculator.log'


def show_last_operations():
    if not os.path.exists(LOG_FILE):
        print("Лог-файл пуст")
        return

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        print("Лог-файл пуст")
    else:
        print("\n--- Последние 5 операций ---")
        for line in lines[-5:]:
            print(line.strip())


def log_operation(operation, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {operation} = {result}\n")


def clear_log():
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        pass
    print("Лог-файл очищен")


def calculate():
    print("\n" + "=" * 40)
    print("КАЛЬКУЛЯТОР")
    print("Операции: +, -, *, /, log, sin")

    try:
        a = float(input("Введите первое число: "))
        op = input("Введите операцию (+, -, *, /, log, sin): ").lower()

        if op in ['+', '-', '*', '/']:
            b = float(input("Введите второе число: "))

            if op == '+':
                result = a + b
            elif op == '-':
                result = a - b
            elif op == '*':
                result = a * b
            elif op == '/':
                if b == 0:
                    print("Ошибка: деление на ноль!")
                    return
                result = a / b

            operation = f"{a} {op} {b}"

        elif op == 'log':
            if a <= 0:
                print("Ошибка: логарифм от неположительного числа!")
                return
            result = math.log(a)
            operation = f"log({a})"

        elif op == 'sin':
            result = math.sin(math.radians(a))
            operation = f"sin({a})"

        else:
            print("Ошибка: неизвестная операция!")
            return

        print(f"Результат: {result}")
        log_operation(operation, result)

    except ValueError:
        print("Ошибка: введите корректные числа!")


def main():
    while True:
        print("\n" + "=" * 40)
        print("1 - Выполнить операцию")
        print("2 - Показать последние 5 операций")
        print("3 - Очистить лог")
        print("4 - Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            calculate()
        elif choice == '2':
            show_last_operations()
        elif choice == '3':
            clear_log()
        elif choice == '4':
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()