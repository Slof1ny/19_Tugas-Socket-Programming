import socket
import threading
import random
import os

# Function to receive data from the server
def ReceiveData(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass

# Function to run the client
def RunClient():
    # Collect the necessary inputs from the user
    server_ip = input("Server IP (use '127.0.0.1' for localhost): ")
    server_port = int(input("Server Port: "))
    password = input("Password: ")

    server = (server_ip, server_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', random.randint(8000, 9000)))

    # Ask for password and wait for server's response
    s.sendto(password.encode('utf-8'), server)
    response, addr = s.recvfrom(1024)
    response = response.decode('utf-8')
    print(response)

    # Check if the password was accepted
    if "Password accepted" not in response:
        print("Exiting due to incorrect password.")
        s.close()
        return  # Exit if password is wrong

    # Ask for the client's name after password verification
    name = input("Nama: ")

    # Send the client's name to the server
    s.sendto(name.encode('utf-8'), server)

    # Start a thread to receive data from the server
    threading.Thread(target=ReceiveData, args=(s,)).start()

    # Main loop to send messages
    while True:
        data = input()
        if data == 'qqq':
            break
        elif data == '':
            continue
        data = name + ': ' + data
        s.sendto(data.encode('utf-8'), server)

    # Close the socket and exit
    s.sendto(data.encode('utf-8'), server)
    s.close()
    os._exit(1)

if __name__ == '__main__':
    RunClient()
