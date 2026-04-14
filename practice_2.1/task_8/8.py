import os


def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        numbers = f.read().split()

    results = []
    for num_str in numbers:
        num = int(num_str)
        if num % 7 == 0:
            result = num * 100 / (73 ** 2 + 29)
            results.append(f"{num} -> {result:.6f}")

    with open(output_file, 'w') as f:
        for line in results:
            f.write(line + '\n')

    print(f"Найдено чисел, кратных 7: {len(results)}")
    for line in results:
        print(line)


def create_test_file():
    numbers = list(range(1, 101))
    with open('../resource/numbers.txt', 'w') as f:
        f.write(' '.join(map(str, numbers)))
    print("Создан файл numbers.txt с числами от 1 до 100")


if not os.path.exists('../resource/numbers.txt'):
    create_test_file()

process_file('../resource/numbers.txt', '../resource/result_8.txt')