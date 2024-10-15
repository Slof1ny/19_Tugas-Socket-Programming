import socket
import threading
import queue
import os
import random
import string

messages = queue.Queue()
clients = []
client_addresses = []
chatroom_password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
print(f"Chatroom password: {chatroom_password}")

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))


def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            if addr not in client_addresses:
                # Expecting the first message to be the password
                if message.decode() == chatroom_password:
                    client_addresses.append(addr)
                    server.sendto("Password accepted. Welcome to the chatroom.".encode(), addr)
                else:
                    server.sendto("Incorrect password. Connection refused.".encode(), addr)
            else:
                messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode())
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                if client != addr:
                    server.sendto(message, client)

def main():
    receive_thread = threading.Thread(target=receive)
    broadcast_thread = threading.Thread(target=broadcast)
    receive_thread.start()
    broadcast_thread.start()
    receive_thread.join()
    broadcast_thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Server is shutting down...")