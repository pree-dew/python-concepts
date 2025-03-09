import socket
import time

def start_blocking_server():
    server = socket.socket()
    server.bind(('127.0.0.1', 12345))
    server.listen(2)
    # By default socket is blocking, or explicitly:
    server.setblocking(True)
    
    print("Blocking server started...")
    
    while True:
        # Will block here until client connects
        print("Waiting for connection...")
        client, addr = server.accept()  # Blocks until client connects
        print(f"Accepted connection from {addr}")
        
        # Will block here until data arrives
        data = client.recv(1024)  # Blocks until data arrives
        print(f"Received: {data.decode()}")
        
        client.send(b"Got your message!")
        client.close()

    server.close()

def start_nonblocking_server():
    server = socket.socket()
    server.bind(('127.0.0.1', 12345))
    server.listen(2)
    server.setblocking(False)
    
    print("Non-blocking server started...")
    
    clients = []
    
    while True:
        try:
            # Won't block, raises error if no connection
            client, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client.setblocking(False)
            clients.append(client)
        except BlockingIOError:
            pass
            
        # Check all clients for data
        for client in clients[:]:
            try:
                data = client.recv(1024)  # Won't block
                if data:
                    print(f"Received: {data.decode()}")
                    client.send(b"Got your message!")
                    clients.remove(client)
                    client.close()
            except BlockingIOError:
                continue
            
        time.sleep(0.1)

    server.close()

if __name__ == "__main__":
    if input("Blocking or non-blocking server? (b/n): ") == "b":
        start_blocking_server()
    else:
        start_nonblocking_server()

