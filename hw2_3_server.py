# Завдання: Створення Простої Системи Чату з
# Використанням Мікросервісів server.py та client.py.
# Опис:
# Розробіть просту систему чату, яка складається з двох
# мікросервісів: сервера (`server.py`) та клієнта (`client.py`).
# Використовуйте Redis для зберігання повідомлень і статусів
# користувачів.
## Server

import socket
import threading
import redis
import time


def client_login():
    while True:
        try:
            print('waiting for client')
            client, address = server.accept()
            print(f"Connection from {address}")
            name = client.recv(1024).decode()
            clients[client] = name
            for key, value in clients.items():
                print(f'{key}: {value}')
            client.send(f'{name}, welcome to chat'.encode())
            print(f'{name}, welcome to chat')

            thread_chat = threading.Thread(target=message_receiver, args=(client,))
            thread_chat.start()

        except:
            continue


def message_receiver(client):
    while True:
        msg = client.recv(1024).decode()
        if msg == 'exit':
            print(client)
            client.close()
            del clients[client]
            print('client deleted')
            break
        else:
            server_R.lpush('messages', clients[client] + ': ' + msg)


def message_sender():
    while True:
        if server_R.llen('messages'):
            msg = server_R.lrange('messages', -1, -1)
            for user in clients:
                user.send(msg[0].encode())
            server_R.rpop('messages')
        else:
            time.sleep(1)


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET,  # use IP4
                           socket.SOCK_STREAM  # use TCP
                           )
    server.bind(('127.0.0.1', 5000))
    server.listen()

    clients = {}

    server_R = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    thread_main = threading.Thread(target=client_login, args=())
    thread_main.start()

    thread_chat = threading.Thread(target=message_sender, args=())
    thread_chat.start()

    thread_main.join()
