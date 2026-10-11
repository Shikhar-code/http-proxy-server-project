import socket
import threading
from datetime import datetime
from cache import get_response, save_response

HOST="127.0.0.1"
PORT=8080
log_lock=threading.Lock()

def log_request(client_address,host,request_line):
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_lock:
        with open("proxy.log","a") as log_file:
            log_file.write(f"{timestamp} | Client: {client_address[0]}:{client_address[1]} | "f"Host: {host} | {request_line}\n")

def is_blocked(host):
    hostname=host.split(":",1)[0].lower()
    with open("blocked_domains.txt","r") as file:
        for line in file:
            blocked_domain=line.strip().lower()
            if hostname==blocked_domain:
                return True
        return False
    
    
def send_error(client_socket, code, reason,message):
    body=message.encode("utf-8")
    response=f"HTTP/1.1 {code} {reason}\r\n" "Content-Type: text/plain\r\n" f"Content-Length: {len(body)}\r\n" "Connection: close\r\n" "\r\n"
    client_socket.sendall(response.encode("utf-8")+body)

def process_client(client_socket,client_address):
    print(f"connection from {client_address}")
    client_socket.settimeout(10)
    request=client_socket.recv(4096)
    if not request:
        client_socket.close()
        return
    request_text=request.decode()
    print("request recieved")
    print(request_text)
    lines=request_text.split("\r\n")
    host=None
    for line in lines:
        if line.lower().startswith("host:"):
            host=line.split(":",1)[1].strip()
            break
    if host is None:
            send_error(client_socket, 400, "Bad Request", "Host header missing.")
            client_socket.close()
            return
    print(f"Destination host: {host}")
    if ":" in host:
        destination_host,port_text=host.rsplit(":",1)
        try:
            destination_port=int(port_text)
        except ValueError:
            destination_port=None
    else:
        destination_host=host
        destination_port=80
    if not destination_port or destination_port is None or not (1<=destination_port<=65535):
            send_error(client_socket, 400, "Bad Request", "Invalid host or port.")
            client_socket.close()
            return
    log_request(client_address, host, lines[0])
    if is_blocked(host):
        print(f"Blocked request to {host}")
        send_error(client_socket, 403, "Forbidden", "Website blocked by proxy.")
        client_socket.close()
        return
    request_parts=lines[0].split()
    if len(request_parts)!=3:
        send_error(client_socket, 400, "Bad Request", "Invalid HTTP request line.")
        client_socket.close()
        return
    method=request_parts[0].upper()
    url=request_parts[1]
    path=url.split(host,1)[1]
    if path=="":
        path="/"
    lines[0]=f"{request_parts[0]} {path} {request_parts[2]}"
    cache_key=host+path
    if method=="GET":
        cached_response = get_response(cache_key)
        if cached_response is not None:
            print(f"CACHE HIT {cache_key}")
            client_socket.sendall(cached_response)
            client_socket.close()
            return
        
        print(f"CACHE MISS: {cache_key}")
            
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as destination_socket:
        destination_socket.settimeout(10)
        try:
            destination_socket.connect((destination_host, destination_port))
        except (socket.timeout,socket.gaierror,ConnectionError):
                send_error(client_socket, 502, "Bad Gateway", "Cannot reach destination server.")
                destination_socket.close()
                client_socket.close()
                return
        for i in range (len(lines)):
            if lines[i].lower().startswith("proxy-connection:"):
                lines[i]="Connection: close"
        forward_request="\r\n".join(lines)
        destination_socket.sendall(forward_request.encode())
        response_data = bytearray()
        while True:
            response=destination_socket.recv(4096)
            if not response:
                break
            response_data.extend(response)
            client_socket.sendall(response)
        if method=="GET":
            if response_data.startswith(b"HTTP/1.1 200") or response_data.startswith(b"HTTP/1.0 200"):
                save_response(cache_key, response_data)
    client_socket.close()

    
def handle_client(client_socket,client_address):
    try:
        process_client(client_socket,client_address)
    finally:
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