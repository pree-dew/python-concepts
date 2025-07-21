import asyncio
from asyncio import AbstractEventLoop

class HTTPGETProtocol(asyncio.Protocol):
    def __init__(self, host: str, loop: AbstractEventLoop):
        self._host = host
        self.loop = loop
        self._future = loop.create_future()
        self._transport = None
        self._response_buffer: bytes = b''


    async def get_response(self):
        return await self._future

    def _get_request_bytes(self):
        request = f"GET / HTTP/1.1\r\n" \
                f"Connection: close\r\n" \
                f"Host: {self._host}\r\n\r\n"
        return request.encode()

    def connection_made(self, transport):
        print(f"Connection made to host: {self._host}")
        self._transport = transport
        self._transport.write(self._get_request_bytes())

    def data_received(self, data):
        print("Data received")
        self._response_buffer = self._response_buffer + data

    def eof_received(self):
        self._future.set_result(self._response_buffer.decode())
        return False

    def connection_close(self, exec):
        if exec is not None:
            self._future.set_exception(exec)



async def make_request(host, port, loop):
    def protocol_factory():
        return HTTPGETProtocol(host, loop)

    _, protocol = await loop.create_connection(protocol_factory, host=host, port=port)
    return await protocol.get_response()


async def main():
    loop = asyncio.get_running_loop()
    result = await make_request('www.example.com', 80, loop)
    print(result)

asyncio.run(main())


