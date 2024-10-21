import socket
import threading

def ReceiveData(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass

def Authenticate(sock, server):
    while True:
        password = input("Password: ")
        sock.sendto(password.encode('utf-8'), server)
        response, _ = sock.recvfrom(1024)
        response = response.decode('utf-8')
        print(response)
        if "Password accepted" in response:
            break
        elif "Password incorrect" in response:
            print("Incorrect password. Please try again.")
        else:
            print("Unexpected response from server. Exiting.")
            return False
    
    while True:
        action = input("Enter 'register' or 'login': ").lower()
        sock.sendto(action.encode('utf-8'), server)
        response, _ = sock.recvfrom(1024)
        response = response.decode('utf-8')
        print(response)

        if "Enter your name" in response:
            name = input("Name: ")
            sock.sendto(name.encode('utf-8'), server)
            response, _ = sock.recvfrom(1024)
            response = response.decode('utf-8')
            print(response)

            if "Enter your ID" in response:
                id = input("ID: ")
                sock.sendto(id.encode('utf-8'), server)
                response, _ = sock.recvfrom(1024)
                response = response.decode('utf-8')
                print(response)

            if "Welcome" in response or "successful" in response:
                return name
            else:
                print("Authentication failed. Please try again.")
        else:
            print("Unexpected response from server. Exiting.")
            return False

def RunClient():
    server_ip = input("Server IP (use '127.0.0.1' for localhost): ")
    server_port = int(input("Server Port: "))
    server = (server_ip, server_port)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 0))  # Bind to a random available port

    name = Authenticate(s, server)
    if not name:
        s.close()
        return
    print(f"You are now in the chat as {name}. Type 'qqq' to quit.")
    threading.Thread(target=ReceiveData, args=(s,), daemon=True).start()

    while True:
        data = input()
        if data.lower() == 'qqq':
            break
        elif data == '':
            continue
        data = f"{data}"
        s.sendto(data.encode('utf-8'), server)

    s.sendto('qqq'.encode('utf-8'), server)
    s.close()
    print("Disconnected from server.")

if __name__ == '__main__':
    RunClient()