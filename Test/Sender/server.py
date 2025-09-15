import socket

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9991
BUFFER_SIZE = 1024
FILE_PATH = 'encrypted_images/sample1.jp2.enc'

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[+] File Server waiting on port {PORT}...")

        client_socket, client_addr = server_socket.accept()
        print(f"[+] Connection established with {client_addr}")

        try:
            with open(FILE_PATH, 'rb') as file:
                while (chunk := file.read(BUFFER_SIZE)):
                    client_socket.sendall(chunk)
            print("[+] File sent successfully.")
        except FileNotFoundError:
            print(f"[!] File not found: {FILE_PATH}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server()
