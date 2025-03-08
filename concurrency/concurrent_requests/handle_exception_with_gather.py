import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=False)

async def main():
    urls = [
        'http://python.org',
        'http://example.com',
        'http://incorrect-url',
    ]
   
    try:
        results = await fetch_all(urls)
    except aiohttp.ClientError as e:
        print("An error occurred:", e)

    for task in asyncio.tasks.all_tasks():
        print("Task:", task)

asyncio.run(main())
