import socket

HOST = "127.0.0.1"
PORT = 5000


def send_file(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    with open(filename, "rb") as f:
        data = f.read()

    client.send(data)

    response = client.recv(1024)
    print(response.decode())

    client.close()


if __name__ == "__main__":
    file = input("Введите имя файла (.json или .xml): ")
    send_file(file)