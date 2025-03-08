import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    urls = [
        'http://python.org',
        'http://example.com',
        'http://incorrect-url',
    ]
    
    results = await fetch_all(urls)
    for result in results:
        if isinstance(result, Exception):
            print(f'Error: {result}')
        else:
            print("Success: ", len(result), "bytes")


asyncio.run(main())
