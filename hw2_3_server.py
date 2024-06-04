# Завдання 3
# Реалізуйте клієнт-серверний додаток , який дозволяє
# користувачам спілкуватися в одному чаті. Кожен користувач
# входить у чат під своїм логіном та паролем. Повідомлення,
# надіслане в чат, видно всім користувачам чату.
## Server

import socket
import threading
import redis

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
            # old broadcast without Redis
            # thread_chat = threading.Thread(target=message_processor, args=(client,))
            # thread_chat.start()

            message_receiver()
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
            server.lpush('messages',    client+msg)
def message_sender(client):
    while True:
        if server.llen('messages'):
            for user in clients:
                if user != client:
                    user.send(msg.encode())

def message_processor(client):
    while True:
        msg = client.recv(1024).decode()
        if msg == 'exit':
            print(client)
            client.close()
            del clients[client]
            print('client deleted')
            break

        msg = f'{clients[client]} say: ' + msg
        print(msg)

        for user in clients:
            if user != client:
                user.send(msg.encode())


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET,  # use IP4
                           socket.SOCK_STREAM  # use TCP
                           )
    server.bind(('127.0.0.1', 5000))
    server.listen()

    clients = {}

    server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    thread_main = threading.Thread(target=client_login, args=())
    thread_main.start()

    thread_main.join()
