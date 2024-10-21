import socket
import threading
import random
import string
import csv
from datetime import datetime

def load_users():
    users = {}
    try:
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                users[row[0]] = row[1]
    except FileNotFoundError:
        pass
    return users

def save_user(name, id):
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, id])

def generate_id():
    return str(random.randint(1000, 9999))

def write_log(message):
    log_file = "log_server.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    
    with open(log_file, "a") as file:
        file.write(log_message)

def generate_password(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def broadcast(message, sender_addr=None):
    for client in clients:
        if client != sender_addr:
            s.sendto(message.encode('utf-8'), client)

def RunServer():
    host = '127.0.0.1'
    port = 9999
    
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    
    global clients
    clients = {}
    users = load_users()
    
    password = generate_password()
    print(f"Generated Password: {password}")
    write_log(f"Server started. Password: {password}")
    print("Server Started")
    
    while True:
        try:
            data, addr = s.recvfrom(1024)
            data = data.decode('utf-8')
            
            if addr not in clients:
                if data == password:
                    s.sendto("Password accepted. Enter 'register' or 'login':".encode('utf-8'), addr)
                    clients[addr] = None  # Menandai bahwa klien telah melewati tahap password
                else:
                    s.sendto("Incorrect password. Try again.".encode('utf-8'), addr)
            elif addr in clients and clients[addr] is None:
                if data.lower() == 'register':
                    s.sendto("Enter your name:".encode('utf-8'), addr)
                    clients[addr] = 'registering'
                elif data.lower() == 'login':
                    s.sendto("Enter your name:".encode('utf-8'), addr)
                    clients[addr] = 'logging_in'
                else:
                    s.sendto("Invalid command. Use 'register' or 'login'.".encode('utf-8'), addr)
            elif addr in clients and clients[addr] == 'registering':
                name = data
                if name in users:
                    s.sendto("Name already exists. Try logging in.".encode('utf-8'), addr)
                    clients[addr] = None
                else:
                    id = generate_id()
                    users[name] = id
                    save_user(name, id)
                    clients[addr] = name
                    s.sendto(f"Registered. Your ID is {id}. Welcome {name}".encode('utf-8'), addr)
                    write_log(f"{name} joined the chat")
                    print(f"{name} joined the chat")
                    broadcast(f"{name} joined the chat.")
            elif addr in clients and clients[addr] == 'logging_in':
                name = data
                if name not in users:
                    s.sendto("Name not found. Try registering.".encode('utf-8'), addr)
                    clients[addr] = None
                else:
                    s.sendto("Enter your ID:".encode('utf-8'), addr)
                    clients[addr] = ('verifying', name)
            elif addr in clients and isinstance(clients[addr], tuple) and clients[addr][0] == 'verifying':
                _, name = clients[addr]
                id = data
                if users[name] == id:
                    clients[addr] = name
                    s.sendto(f"Login successful. Welcome back, {name}!".encode('utf-8'), addr)
                    write_log(f"{name} joined the chat")
                    print(f"{name} joined the chat")
                    broadcast(f"{name} joined the chat.")
                else:
                    s.sendto("Incorrect ID. Try again.".encode('utf-8'), addr)
                    clients[addr] = None
            else:
                name = clients[addr]
                message = f"{name}: {data}"
                broadcast(message, addr)
                write_log(message)
                print(message)
                
                if data.lower() == 'qqq':
                    write_log(f"{name} left the chat")
                    print(f"{name} left the chat")
                    broadcast(f"{name} left the chat")
                    del clients[addr]

        except Exception as e:
            print(f"An error occurred: {e}")
            write_log(f"Error: {e}")
            print(e)
            print("Server stopped")

if __name__ == '__main__':
    RunServer()