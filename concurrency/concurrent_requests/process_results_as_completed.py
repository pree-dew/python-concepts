import aiohttp
import asyncio

async def fetch(session, url, delay = 0):
    await asyncio.sleep(delay)
    async with session.get(url) as response:
        await response.text()
        return f'{url} status: {response.status}'


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        tasks.append(fetch(session, 'https://httpbin.org/status/200', 5))
        tasks.append(fetch(session, 'https://httpbin.org/status/404', 3))
        tasks.append(fetch(session, 'https://httpbin.org/status/500', 1))

        for task in asyncio.as_completed(tasks, timeout = 20):
            try:
                result = await task
                print(result)
            except asyncio.TimeoutError:
                print('The request timed out')
        
        for task in asyncio.tasks.all_tasks():
            print(task)

asyncio.run(main()) 
