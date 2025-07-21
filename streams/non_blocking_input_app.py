import asyncio
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

async def sleep(n, msg_store: MessageStore):
    await msg_store.append(f"starting sleeping for {n}")
    await asyncio.sleep(n)
    await msg_store.append(f"finished sleeping for {n}")


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

    while True:
        line = await read_line(stdin_reader)
        delay_time = int(line)
        asyncio.create_task(sleep(delay_time, msg_store))


if __name__ == "__main__":
    asyncio.run(main())


