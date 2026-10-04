import socket
HOST="127.0.0.1"
PORT=8080
def main():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(5)
    print(f"server starting on {HOST}:{PORT}")
        
    while True:
            client_socket,client_address=server_socket.accept()
            print(f"connection from {client_address}")
            request=client_socket.recv(4096)
            print("request recieved")
            print(request.decode())
            client_socket.close()
    
if __name__== "__main__":
    main()  