import requests

BASE_URL = "https://api.github.com"


def get_user(username):
    r = requests.get(f"{BASE_URL}/users/{username}")
    data = r.json()

    print("Имя:", data.get("name"))
    print("Профиль:", data.get("html_url"))
    print("Репозитории:", data.get("public_repos"))
    print("Подписки:", data.get("following"))
    print("Подписчики:", data.get("followers"))


def get_repos(username):
    r = requests.get(f"{BASE_URL}/users/{username}/repos")
    repos = r.json()

    for repo in repos:
        print("\nНазвание:", repo["name"])
        print("Ссылка:", repo["html_url"])
        print("Язык:", repo["language"])
        print("Видимость:", "private" if repo["private"] else "public")
        print("Ветка:", repo["default_branch"])


def search_repo(name):
    r = requests.get(f"{BASE_URL}/search/repositories?q={name}")
    data = r.json()["items"]

    for repo in data[:5]:
        print(repo["name"], "-", repo["html_url"])


if __name__ == "__main__":
    while True:
        print("\n1 - Профиль")
        print("2 - Репозитории")
        print("3 - Поиск")
        print("0 - Выход")

        c = input("Выбор: ")

        if c == "1":
            user = input("Username: ")
            get_user(user)
        elif c == "2":
            user = input("Username: ")
            get_repos(user)
        elif c == "3":
            name = input("Название: ")
            search_repo(name)
        elif c == "0":
            break