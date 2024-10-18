import socket
import threading
import random
import string
import os
from datetime import datetime

def write_log(message):
    log_file = "log_server.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    
    with open(log_file, "a") as file:
        file.write(log_message)

def generate_password(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def broadcast(message, sender_addr, clients):
    for addr, client in clients.items():
        if addr != sender_addr and client['authenticated']:
            try:
                server_socket.sendto(message.encode('utf-8'), addr)
            except:
                pass

def handle_client(data, addr, clients, password):
    if addr not in clients:
        clients[addr] = {'authenticated': False, 'name': None}

    if not clients[addr]['authenticated']:
        if data.decode('utf-8') == password:
            server_socket.sendto("Password accepted. Please enter your name.".encode('utf-8'), addr)
            clients[addr]['authenticated'] = True
            write_log(f"Client {addr} authenticated successfully")
        else:
            server_socket.sendto("Password incorrect. Please try again.".encode('utf-8'), addr)
            write_log(f"Failed authentication attempt from {addr}")
    elif clients[addr]['name'] is None:
        name = data.decode('utf-8')
        if any(client['name'] == name for client in clients.values()):
            server_socket.sendto("Name is already taken. Please choose a different name.".encode('utf-8'), addr)
        else:
            clients[addr]['name'] = name
            welcome_message = f"Welcome {name}! You can start chatting."
            server_socket.sendto(welcome_message.encode('utf-8'), addr)
            broadcast(f"{name} has joined the chat!", addr, clients)
            print(f"New client {addr} joined as {name}")
            write_log(f"New client {addr} joined as {name}")
    else:
        message = data.decode('utf-8')
        if message.lower() == 'qqq':
            broadcast(f"{clients[addr]['name']} has left the chat.", addr, clients)
            print(f"Client {clients[addr]['name']} disconnected")
            del clients[addr]
        else:
            broadcast(f"{clients[addr]['name']}: {message}", addr, clients)
            print(f"{clients[addr]['name']}: {message}")
            write_log(f"{clients[addr]['name']}: {message}")

def start_server():
    global server_socket
    host = '127.0.0.1'
    port = 9999
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    clients = {}
    password = generate_password()
    print(f"Server started. Password is: {password}")
    print('Server hosting on IP -> ' + str(host))
    print('Server running on port -> ' + str(port))
    print('Server password -> ' + str(password))
    write_log("Server started")
    write_log(f"Server IP: {host}, Port: {port}")

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            threading.Thread(target=handle_client, args=(data, addr, clients, password)).start()
        except:
            pass

if __name__ == '__main__':
    start_server()