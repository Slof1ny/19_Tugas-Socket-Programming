import socket
import threading
import queue
import random
import string

def RecvData(sock, recvPackets):
    while True:
        data, addr = sock.recvfrom(1024)
        recvPackets.put((data, addr))
# Function to generate a random 6-character alphanumeric password
def generate_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def RunServer():
    host = '127.0.0.1'
    port = 9999
    password = generate_password()  # Generate 6-character password
    print('Server hosting on IP -> ' + str(host))
    print('Server running on port -> ' + str(port))
    print('Server password -> ' + str(password))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    
    clients = {}  # Dictionary untuk menyimpan alamat klien dan status autentikasi
    recvPackets = queue.Queue()

    print('Server Running...')

    threading.Thread(target=RecvData, args=(s, recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data, addr = recvPackets.get()
            data = data.decode('utf-8')

            if addr not in clients:
                # Proses autentikasi
                if data == password:
                    s.sendto("Password accepted. Please enter your name.".encode('utf-8'), addr)
                    clients[addr] = {'authenticated': False, 'name': None}
                else:
                    s.sendto("Invalid password. Try again.".encode('utf-8'), addr)
            elif not clients[addr]['authenticated']:
                # Proses penerimaan nama
                clients[addr]['name'] = data
                clients[addr]['authenticated'] = True
                s.sendto(f"Welcome {data}! You can start chatting.".encode('utf-8'), addr)
                print(f"New client {addr} joined as {data}")
            else:
                # Proses chat biasa
                if data == 'qqq':
                    print(f"Client {clients[addr]['name']} disconnected")
                    del clients[addr]
                else:
                    print(f"{data}")
                    for client in clients:
                        if client != addr and clients[client]['authenticated']:
                            s.sendto(f"{data}".encode('utf-8'), client)

    s.close()

if __name__ == '__main__':
    RunServer()