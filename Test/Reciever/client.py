import socket

BUFFER_SIZE = 1024
SAVE_AS = 'received_sample1.jp2.enc'

def start_client(server_ip, port=9991):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((server_ip, port))
            print(f"[+] Connected to server at {server_ip}:{port}")

            with open(SAVE_AS, 'wb') as file:
                while True:
                    data = client_socket.recv(BUFFER_SIZE)
                    if not data:
                        break
                    file.write(data)

            print(f"[+] File received and saved as '{SAVE_AS}'")
        except Exception as e:
            print(f"[!] Connection error: {e}")

if __name__ == "__main__":
    ip = input("Enter server IP address: ")
    start_client(ip)
