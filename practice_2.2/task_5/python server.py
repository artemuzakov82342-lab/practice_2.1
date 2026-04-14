import socket

HOST = "127.0.0.1"
PORT = 5000
KEY = 42  # ключ шифрования


def xor_encrypt(data: bytes) -> bytes:
    return bytes([b ^ KEY for b in data])


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Сервер запущен...")

while True:
    conn, addr = server.accept()
    print("Подключен:", addr)

    try:
        data = conn.recv(100000)

        # проверка формата (очень простая)
        text = data.decode(errors="ignore")

        if not (text.strip().startswith("{") or text.strip().startswith("<")):
            conn.send(b"ERROR: only JSON or XML allowed")
            conn.close()
            continue

        encrypted = xor_encrypt(data)

        with open("../resource/file.bin", "wb") as f:
            f.write(encrypted)

        conn.send(b"OK: file saved and encrypted")

    except Exception as e:
        conn.send(f"ERROR: {e}".encode())

    conn.close()