import struct
import os


def parse_binary_file(filename='data.bin'):
    if not os.path.exists(filename):
        create_test_binary_file(filename)

    with open(filename, 'rb') as f:
        signature = f.read(4)
        if signature != b'DATA':
            print(f"Ошибка: неверная сигнатура {signature}")
            return

        version = struct.unpack('<H', f.read(2))[0]
        count = struct.unpack('<I', f.read(4))[0]

        print(f"Сигнатура: {signature}")
        print(f"Версия: {version}")
        print(f"Количество записей: {count}")
        print("=" * 50)

        temperatures = []
        active_flags = 0

        for i in range(count):
            data = f.read(15)
            if len(data) < 15:
                print(f"Ошибка: файл поврежден, запись {i + 1} неполная")
                break

            timestamp, record_id, temp_raw, flag = struct.unpack('<Q I h B', data)
            temperature = temp_raw / 100.0
            temperatures.append(temperature)

            if flag & 1:
                active_flags += 1

            print(f"Запись {i + 1}:")
            print(f"  Timestamp: {timestamp}")
            print(f"  ID: {record_id}")
            print(f"  Температура: {temperature:.2f}°C")
            print(f"  Флаг: {flag:08b}")
            print()

        print("=" * 50)
        print("СТАТИСТИКА:")
        if temperatures:
            avg_temp = sum(temperatures) / len(temperatures)
            print(f"  Средняя температура: {avg_temp:.2f}°C")
            print(f"  Минимальная: {min(temperatures):.2f}°C")
            print(f"  Максимальная: {max(temperatures):.2f}°C")
        print(f"  Активных флагов: {active_flags} из {count}")


def create_test_binary_file(filename='data.bin'):
    with open(filename, 'wb') as f:
        f.write(b'DATA')
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<I', 5))
        f.write(struct.pack('<Q I h B', 1700000000, 101, 2250, 0b00000001))
        f.write(struct.pack('<Q I h B', 1700000100, 102, -500, 0b00000000))
        f.write(struct.pack('<Q I h B', 1700000200, 103, 3500, 0b00000011))
        f.write(struct.pack('<Q I h B', 1700000300, 104, 2200, 0b00000010))
        f.write(struct.pack('<Q I h B', 1700000400, 105, 2800, 0b00000101))


parse_binary_file('../resource/data.bin')