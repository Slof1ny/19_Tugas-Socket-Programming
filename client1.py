import socket
import threading
import rsa_cipher
from rsa_cipher import encrypt, decrypt

def ReceiveData(sock, private_key):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            encrypted_message_str = data.decode('utf-8')
            encrypted_message = list(map(int, encrypted_message_str.split()))  # Convert back to list of integers
            decrypted_message = decrypt(private_key, encrypted_message)
            print(decrypted_message)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def Authenticate(sock, server):
    public_key = None
    while True:
        password = input("Password: ")
        sock.sendto(password.encode('utf-8'), server)
        response, _ = sock.recvfrom(1024)
        response = response.decode('utf-8')
        print(response)

        if response.startswith("(") and response.endswith(")"):
            # Attempt to parse the tuple from the string
            try:
                public_key_str = response.strip("()")  # Remove the parentheses
                e, n = map(int, public_key_str.split(","))
                public_key = (e, n)
            except ValueError:
                public_key = None
        if isinstance(public_key, tuple):
            print(f"Public key received: {public_key}")
            break
        elif response == "Incorrect password. Try again.":
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
                return f"Logged in successfull, welcome {name}. public key is {public_key}"
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

    
    auth_response = Authenticate(s, server)
    if not auth_response:
        s.close()
        return

    public_key_str = auth_response.split("public key is ")[1]
    e, n = map(int, public_key_str.strip("()").split(", "))
    public_key = (e, n)

    name = auth_response.split("welcome ")[1]
    print(f"You are now in the chat as {name}. Type 'qqq' to quit.")
    threading.Thread(target=ReceiveData, args=(s, public_key), daemon=True).start()

    while True:
        data = input()
        if data.lower() == 'qqq':
            break
        elif data == '':
            continue
        message = encrypt(public_key, data)
        s.sendto(str(message).encode('utf-8'), server)

    s.sendto('qqq'.encode('utf-8'), server)
    s.close()
    print("Disconnected from server.")

if __name__ == '__main__':
    RunClient()