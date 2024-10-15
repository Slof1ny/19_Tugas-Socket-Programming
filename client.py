import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))

server_ip = input("Server IP: ")
server_port = int(input("Server Port: "))
name = input("Nama: ")
password = input("Password: ")

# Function to receive messages
def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

# Start the receive thread
t = threading.Thread(target=receive)
t.start()

# Send password to server
client.sendto(password.encode(), (server_ip, server_port))

# Wait for server response
response, _ = client.recvfrom(1024)
print(response.decode())

if "accepted" in response.decode():
    # Main loop to send messages
    while True:
        message = input("")
        client.sendto(f"{name}: {message}".encode(), (server_ip, server_port))
else:
    print("Failed to join the chatroom. Exiting...")
