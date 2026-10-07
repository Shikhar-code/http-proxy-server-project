import socket
import threading
import time
HOST="127.0.0.1"
PORT=8080

def handle_client(client_socket,client_address):
    print(f"connection from {client_address}")
    time.sleep(5)
    request=client_socket.recv(4096)
    request_text=request.decode()
    print("request recieved")
    print(request_text)
    lines=request_text.split("\r\n")
    host=None
    for line in lines:
        if line.lower().startswith("host:"):
            host=line.split(":",1)[1].strip()
            break
    print(f"Destination host: {host}")
    request_parts=lines[0].split()
    url=request_parts[1]
    path=url.split(host,1)[1]
    if path=="":
        path="/"
    lines[0]=f"{request_parts[0]} {path} {request_parts[2]}"
    destination_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    destination_socket.connect((host,80))
    for i in range (len(lines)):
        if lines[i].lower().startswith("proxy-connection:"):
            lines[i]="Connection: close"
    forward_request="\r\n".join(lines)
    destination_socket.sendall(forward_request.encode())
    while True:
        response=destination_socket.recv(4096)
        if not response:
            break
        client_socket.sendall(response)
    destination_socket.close()
    client_socket.close()

    
    

def main():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(5)
    print(f"server starting on {HOST}:{PORT}")
        
    while True:
            client_socket,client_address=server_socket.accept()
            client_thread=threading.Thread(target=handle_client,args=(client_socket,client_address))    
            client_thread.start()    
if __name__== "__main__":
    main()  