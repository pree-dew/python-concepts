import asyncio
import time

async def delayed_message(delay, message):
    await asyncio.sleep(delay)
    print(message)

async def main():
    r1 = asyncio.create_task(delayed_message(10, "one"))

    try:
        await asyncio.wait_for(r1, timeout=5)
    except asyncio.TimeoutError:
        print("timeout")
        print("is task r1 cancelled? ", r1.cancelled())

start = time.time()
asyncio.run(main())
print("Elapsed time: ", time.time() - start)
