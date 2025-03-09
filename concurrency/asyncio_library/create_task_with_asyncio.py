import asyncio
import time

async def delayed_message(delay, message):
    await asyncio.sleep(delay)
    print(message)

async def main():
    r1 = asyncio.create_task(delayed_message(3, "one"))
    r2 = asyncio.create_task(delayed_message(3, "two"))
    await r1
    await r2

start = time.time()
asyncio.run(main())
print("Elapsed time: ", time.time() - start)
