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


if __name__ == "__main__":
    start_blocking_server()

