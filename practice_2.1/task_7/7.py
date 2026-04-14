import os

KEY = 0xAB


def rotate_left(byte, bits):
    bits = bits % 8
    return ((byte << bits) | (byte >> (8 - bits))) & 0xFF


def rotate_right(byte, bits):
    bits = bits % 8
    return ((byte >> bits) | (byte << (8 - bits))) & 0xFF


def encrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted = bytearray()
    for byte in data:
        step1 = rotate_left(byte, 2)
        step2 = step1 ^ KEY
        encrypted.append(step2)

    with open(output_file, 'wb') as f:
        f.write(encrypted)

    print(f"Зашифровано: {output_file}")


def decrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()

    decrypted = bytearray()
    for byte in data:
        step1 = byte ^ KEY
        step2 = rotate_right(step1, 2)
        decrypted.append(step2)

    with open(output_file, 'wb') as f:
        f.write(decrypted)

    print(f"Расшифровано: {output_file}")


def create_test_file():
    content = b"Hello World! This is a test file for encryption."
    with open('../resource/test.txt', 'wb') as f:
        f.write(content)
    print("Создан test.txt")


if not os.path.exists('../resource/test.txt'):
    create_test_file()

encrypt_file('../resource/test.txt', '../resource/test_encrypted.bin')
decrypt_file('../resource/test_encrypted.bin', '../resource/test_decrypted.txt')

with open('../resource/test_decrypted.txt', 'rb') as f:
    print(f"Результат: {f.read().decode()}")