import asyncio
import asyncpg
import os
import sys
import tty
import shutil

from asyncio import StreamReader
from collections import deque

def save_cursor_position():
    sys.stdout.write('\0337')

def restore_cursor_position():
    sys.stdout.write('\0338')

def move_to_top_of_screen():
    sys.stdout.write('\033[H')

def delete_line():
    sys.stdout.write('\033[2K')

def clear_line():
    sys.stdout.write('\033[2K\033[0G')

def move_back_one_char():
    sys.stdout.write('\033[1D')

def move_to_bottom_of_screen():
    _, total_rows = shutil.get_terminal_size()
    input_row = total_rows - 1
    sys.stdout.write(f'\033[{input_row}E')
    return total_rows

async def create_stdin_reader():
    stream_reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(stream_reader)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return stream_reader

class MessageStore:
    def __init__(self, rows, callback):
        self._deque = deque(maxlen=rows)
        self._callback = callback

    async def append(self, msg):
        self._deque.append(msg)
        await self._callback(self._deque)

async def run_query(query, pool, msg_store):
    async with pool.acquire() as connection:
        try:
            result = await connection.fetchrow(query)
            await msg_store.append(f'Fetched {len(result)} for query {query}')
        except Exception as e:
            await msg_store.append(f'Got exception {e} for query {query}')
            
async def read_line(stdin_reader: StreamReader) -> str:
    def erase_last_char():
        move_back_one_char()
        sys.stdout.write(' ')
        move_back_one_char()

    delete_char = b'\x7f'
    input_buffer = deque()
    while (char := await stdin_reader.read(1)) != b'\n':
        if char == delete_char:
            if len(input_buffer) > 0:
                input_buffer.pop()
                erase_last_char()
                sys.stdout.flush()
        else:
            input_buffer.append(char)
            sys.stdout.write(char.decode())
            sys.stdout.flush()
    clear_line()
    
    return b''.join(input_buffer).decode()

async def main():
    tty.setcbreak(sys.stdin)
    os.system('clear')
    rows = move_to_bottom_of_screen()

    async def redraw_screen(items: deque):
        save_cursor_position()
        move_to_top_of_screen()
        for item in items:
            delete_line()
            print(item)

        restore_cursor_position()

    msg_store = MessageStore(rows - 1, redraw_screen)

    stdin_reader = await create_stdin_reader()

    async with asyncpg.create_pool(host='127.0.0.1',
                                   port=5432,
                                   user='postgres',
                                   password='postgres',
                                   database='postgres',
                                   min_size=6,
                                   max_size=6) as pool:
        while True:
            query = await read_line(stdin_reader)
            asyncio.create_task(run_query(query, pool, msg_store))

if __name__ == "__main__":
    asyncio.run(main())


