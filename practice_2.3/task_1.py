import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import psutil
import json
import socket

SAVE_FILE = "../practice_2.2/resource/save.json"

HOST = "127.0.0.1"
PORT = 5000


#--------------------САЙТЫ--------------------

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


def check_sites():
    urls = [
        "https://github.com/",
        "https://www.binance.com/en",
        "https://tomtit.tomsk.ru/",
        "https://jsonplaceholder.typicode.com/",
        "https://moodle.tomtit-tomsk.ru/"
    ]

    result_text.delete(1.0, tk.END)

    for url in urls:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=5)

            result_text.insert(
                tk.END,
                f"{url} — {get_status(r.status_code)} — {r.status_code}\n"
            )

        except:
            result_text.insert(tk.END, f"{url} — не доступен — ошибка\n")


#--------------------СИСТЕМА--------------------

def update_system():
    cpu_label.config(text=f"CPU: {psutil.cpu_percent()}%")
    ram_label.config(text=f"RAM: {psutil.virtual_memory().percent}%")
    disk_label.config(text=f"Disk: {psutil.disk_usage('/').percent}%")
    root.after(1000, update_system)


#--------------------ВАЛЮТЫ--------------------

def get_currency_data():
    return requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()


def load_groups():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_groups(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def show_all_currency():
    data = get_currency_data()["Valute"]
    currency_text.delete(1.0, tk.END)

    for k, v in data.items():
        currency_text.insert(tk.END, f"{k}: {v['Value']}\n")


def show_one_currency():
    code = currency_entry.get().upper()
    data = get_currency_data()["Valute"]

    currency_text.delete(1.0, tk.END)

    if code in data:
        currency_text.insert(tk.END, f"{code}: {data[code]['Value']}")
    else:
        currency_text.insert(tk.END, "Не найдено")


def create_group():
    name = group_entry.get()
    groups = load_groups()

    if name in groups:
        messagebox.showwarning("Ошибка", "Группа уже существует")
        return

    groups[name] = []
    save_groups(groups)
    messagebox.showinfo("OK", "Группа создана")


def add_currency():
    group = group_entry.get()
    code = currency_entry.get().upper()

    groups = load_groups()

    if group in groups:
        groups[group].append(code)
        save_groups(groups)
        messagebox.showinfo("OK", "Добавлено")
    else:
        messagebox.showerror("Ошибка", "Группа не найдена")


def remove_currency():
    group = group_entry.get()
    code = currency_entry.get().upper()

    groups = load_groups()

    if group in groups and code in groups[group]:
        groups[group].remove(code)
        save_groups(groups)
        messagebox.showinfo("OK", "Удалено")
    else:
        messagebox.showerror("Ошибка", "Не найдено")


def show_groups():
    groups = load_groups()
    currency_text.delete(1.0, tk.END)

    for g, vals in groups.items():
        currency_text.insert(tk.END, f"{g}: {vals}\n")


#--------------------ГИТХАб--------------------

def get_user():
    username = github_entry.get()

    r = requests.get(f"https://api.github.com/users/{username}")
    data = r.json()

    github_text.delete(1.0, tk.END)

    github_text.insert(tk.END, f"Имя: {data.get('name')}\n")
    github_text.insert(tk.END, f"Профиль: {data.get('html_url')}\n")
    github_text.insert(tk.END, f"Репо: {data.get('public_repos')}\n")
    github_text.insert(tk.END, f"Подписчики: {data.get('followers')}\n")


def get_repos():
    username = github_entry.get()

    r = requests.get(f"https://api.github.com/users/{username}/repos")
    repos = r.json()

    github_text.delete(1.0, tk.END)

    for repo in repos:
        github_text.insert(tk.END, f"\n{repo['name']}\n{repo['html_url']}\n")


def search_repo():
    name = search_entry.get()

    r = requests.get(f"https://api.github.com/search/repositories?q={name}")
    data = r.json()["items"]

    github_text.delete(1.0, tk.END)

    for r in data[:10]:
        github_text.insert(tk.END, f"{r['name']} — {r['html_url']}\n")


#--------------------Сервер--------------------

def send_file_to_server():
    filepath = filedialog.askopenfilename(
        filetypes=[("JSON/XML files", "*.json *.xml")]
    )

    if not filepath:
        return

    try:
        server_status.config(text="Отправка...", fg="orange")
        root.update_idletasks()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(5)
            client.connect((HOST, PORT))

            with open(filepath, "rb") as f:
                data = f.read()

            client.sendall(data)

            response = client.recv(4096).decode(errors="ignore")

        server_text.delete(1.0, tk.END)
        server_text.insert(tk.END, response)

        # ✔ успех
        server_status.config(
            text="✔ Файл успешно отправлен!",
            fg="green"
        )

    except ConnectionRefusedError:
        server_text.delete(1.0, tk.END)
        server_text.insert(tk.END, "Сервер не запущен")

        server_status.config(
            text="✖ Сервер не запущен",
            fg="red"
        )

    except Exception as e:
        server_text.delete(1.0, tk.END)
        server_text.insert(tk.END, f"Ошибка: {e}")

        server_status.config(
            text="✖ Ошибка отправки файла",
            fg="red"
        )


#------------------------------------------------------------ОКНО ПРИЛОЖЕНИЯ------------------------------------------------------------

root = tk.Tk()
root.title("Практика 2.3")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)


#--------------------Сайты--------------------

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="HTTP")

tk.Button(tab1, text="Чекнуть сайты", command=check_sites).pack()
result_text = tk.Text(tab1)
result_text.pack(fill="both", expand=True)


#--------------------Система--------------------

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Система")

cpu_label = tk.Label(tab2, text="CPU")
cpu_label.pack()

ram_label = tk.Label(tab2, text="RAM")
ram_label.pack()

disk_label = tk.Label(tab2, text="Disk")
disk_label.pack()

update_system()


#--------------------Валюты--------------------

tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Валюты")

tab3.rowconfigure(8, weight=1)
tab3.columnconfigure(1, weight=1)

tk.Label(tab3, text="Название валюты").grid(row=0, column=0, padx=5, pady=5, sticky="w")
currency_entry = tk.Entry(tab3, width=30)
currency_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(tab3, text="Название группы").grid(row=1, column=0, padx=5, pady=5, sticky="w")
group_entry = tk.Entry(tab3, width=30)
group_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Button(tab3, text="Все валюты", width=20, command=show_all_currency)\
    .grid(row=2, column=0, padx=5, pady=3, sticky="w")

tk.Button(tab3, text="Поиск по названию", width=20, command=show_one_currency)\
    .grid(row=3, column=0, padx=5, pady=3, sticky="w")

tk.Button(tab3, text="Создать группу", width=20, command=create_group)\
    .grid(row=4, column=0, padx=5, pady=3, sticky="w")

tk.Button(tab3, text="Добавить валюту", width=20, command=add_currency)\
    .grid(row=5, column=0, padx=5, pady=3, sticky="w")

tk.Button(tab3, text="Удалить валюту", width=20, command=remove_currency)\
    .grid(row=6, column=0, padx=5, pady=3, sticky="w")

tk.Button(tab3, text="Показать группы", width=20, command=show_groups)\
    .grid(row=7, column=0, padx=5, pady=3, sticky="w")

currency_text = tk.Text(tab3)
currency_text.grid(row=2, column=1, rowspan=6, padx=5, pady=5, sticky="nsew")


#--------------------ГИТХАБ--------------------

tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="GitHub")

tab4.rowconfigure(5, weight=1)
tab4.columnconfigure(1, weight=1)

tk.Label(tab4, text="Имя пользователя").grid(row=0, column=0, sticky="w", padx=5, pady=2)
github_entry = tk.Entry(tab4, width=30)
github_entry.grid(row=0, column=1, sticky="w")

tk.Label(tab4, text="Репозиторий").grid(row=1, column=0, sticky="w", padx=5, pady=2)
search_entry = tk.Entry(tab4, width=20)
search_entry.grid(row=1, column=1, sticky="w")

tk.Button(tab4, text="Профиль", command=get_user)\
    .grid(row=0, column=2, padx=(0,400), pady=5, sticky="w")

tk.Button(tab4, text="Репозитории", command=get_repos)\
    .grid(row=2, column=0, padx=(5), pady=5, sticky="w")

tk.Button(tab4, text="Поиск", command=search_repo)\
    .grid(row=1, column=2, padx=(0,400), pady=5, sticky="w")

github_text = tk.Text(tab4)
github_text.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)


#--------------------СЕРВЕР--------------------

tab5 = ttk.Frame(notebook)
notebook.add(tab5, text="Server")

tab5.rowconfigure(3, weight=1)
tab5.columnconfigure(0, weight=1)

tk.Label(tab5, text="Клиент - сервер")\
    .grid(row=0, column=0, sticky="w", padx=5, pady=5)

tk.Button(tab5, text="Выбрать файл и отправить на сервер", command=send_file_to_server)\
    .grid(row=1, column=0, sticky="w", padx=5, pady=5)

server_status = tk.Label(tab5, text="", fg="green")
server_status.grid(row=2, column=0, sticky="w", padx=5, pady=2)

server_text = tk.Text(tab5)
server_text.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)


root.mainloop()