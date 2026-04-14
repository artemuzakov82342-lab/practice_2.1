import requests

urls = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]

def get_status(code):
    if code == 200:
        return "доступен"
    elif code == 403:
        return "вход запрещен"
    elif code == 404:
        return "не найден"
    elif code >= 500:
        return "ошибка сервера"
    else:
        return "не доступен"


def check_site(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=5)
        code = response.status_code

        status = get_status(code)

        print(f"{url} — {status} — {code}")

    except requests.exceptions.Timeout:
        print(f"{url} — не доступен — таймаут")

    except requests.exceptions.ConnectionError:
        print(f"{url} — не доступен — ошибка соединения")

    except Exception as e:
        print(f"{url} — ошибка — {e}")


for url in urls:
    check_site(url)