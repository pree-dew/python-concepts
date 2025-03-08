import aiohttp
import asyncio

async def fetch(session, url, delay=0):
    await asyncio.sleep(delay)
    async with session.get(url) as response:
        await response.text()
        return response.status

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(fetch(session, 'python://org', 1)),
            asyncio.create_task(fetch(session, 'http://httpbin.org/delay/2', 5)),
            asyncio.create_task(fetch(session, 'http://httpbin.org/delay/1', 1)),
        ]

        
        done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

        print("Done tasks: ",len(done))
        print("Pending tasks: ",len(pending))

        for done_task in done:
            if done_task.exception():
                print(f"Task error: {done_task.exception()}")
                continue

            print(f"Task result: {done_task.result()}")

asyncio.run(main())
        

