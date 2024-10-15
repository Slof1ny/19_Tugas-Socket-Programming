import socket
import threading
import queue
import random
import string

# Function to receive data from clients
def RecvData(sock, recvPackets):
    while True:
        data, addr = sock.recvfrom(1024)
        recvPackets.put((data, addr))

# Function to generate a random 6-character alphanumeric password
def generate_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Function to run the server
def RunServer():
    host = '127.0.0.1'
    port = 9999
    password = generate_password()  # Generate 6-character password
    print('Server hosting on IP -> ' + str(host))
    print('Server password -> ' + password)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    
    clients = set()
    recvPackets = queue.Queue()

    print('Server Running...')

    threading.Thread(target=RecvData, args=(s, recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data, addr = recvPackets.get()
            data = data.decode('utf-8')

            # Handle client connection verification with password
            if addr not in clients:
                if data == password:
                    clients.add(addr)
                    s.sendto("Password accepted. Welcome to the chatroom.".encode('utf-8'), addr)
                    print(f"Client {addr} connected.")
                else:
                    s.sendto("Incorrect password. Connection refused.".encode('utf-8'), addr)
                    print(f"Client {addr} failed to connect due to wrong password.")
                    continue

            # Handle normal client communication
            if data.endswith('qqq'):
                clients.remove(addr)
                continue
            
            print(str(addr) + ' -> ' + data)
            for c in clients:
                if c != addr:
                    s.sendto(data.encode('utf-8'), c)
    s.close()

if __name__ == '__main__':
    RunServer()
