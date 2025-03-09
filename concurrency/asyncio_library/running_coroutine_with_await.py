import asyncio
import time

async def delayed_message(delay, message):
    await asyncio.sleep(delay)
    print(message)

async def main():
    await delayed_message(3, "one")
    await delayed_message(3, "two")

start = time.time()
asyncio.run(main())
print("Elapsed time: ", time.time() - start)
