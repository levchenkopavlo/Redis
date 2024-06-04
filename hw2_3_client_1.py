## Client

import socket
import threading


def msg_send():
    while True:
        msg = input(f'{name}. Enter message: \n')

        client.send(msg.encode())
        if msg == 'exit':
            # thread_receive.join()
            client.close()
            quit()

def msg_receive():
    while True:
        try:
            print(client.recv(1024).decode())
        except:
            break

if __name__ == "__main__":

    client = socket.socket(socket.AF_INET,  # use IP4
                           socket.SOCK_STREAM  # use TCP
                           )

    client.connect(('127.0.0.1', 5000))

    while True:
        name = input("Enter your name: ")
        if not name:
            print('Name can not be empty.')
            continue
        client.send(name.encode())
        response = client.recv(1024).decode()
        break

    if 'welcome' in response:
        print('You authorized.')
        print(response)

        thread_send = threading.Thread(target=msg_send, args=())
        thread_send.start()

        thread_receive = threading.Thread(target=msg_receive, args=())
        thread_receive.start()

        thread_send.join()
