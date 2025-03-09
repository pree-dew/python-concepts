import asyncio
import socket

class AsynchronousContextManager:
    def __init__(self, sock):
        self.sock = sock
    
    # accepts a connection
    async def __aenter__(self):
        print('Entering context manager')
        loop = asyncio.get_event_loop()
        self.conn, _ = await loop.sock_accept(self.sock)
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        print('Exiting context manager')
        self.conn.close()
        return True


async def main():
    loop = asyncio.get_event_loop()
    # create a socket server
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 25000))
    sock.listen()
    sock.setblocking(False)

    async with AsynchronousContextManager(sock) as conn:
        data = await loop.sock_recv(conn, 1024)
        print(data)

asyncio.run(main())

