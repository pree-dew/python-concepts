import asyncio
import time

async def delayed_message(delay, message):
    await asyncio.sleep(delay)
    print(message)

async def main():
    r1 = asyncio.create_task(delayed_message(10, "one"))

    while r1.done() == False:
        print("running for ", (time.time() - start).__round__())
        await asyncio.sleep(1)
        if second_passed := time.time() - start > 5:
            print("cancelling task")
            r1.cancel()
            
    try:
        await r1
    except asyncio.CancelledError:
        print("cancelled")

start = time.time()
asyncio.run(main())
print("Elapsed time: ", time.time() - start)
