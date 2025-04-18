import asyncio
import aiohttp
import time

def async_timed():
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            await func(*args, **kwargs)
            end_time = time.time()
            print(f'Execution time of {func} is {end_time - start_time} seconds')
        return wrapper
    return decorator

@async_timed()
async def make_request():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.google.com') as response:
            await response.text()


@async_timed()
async def main():
    t1 = asyncio.create_task(make_request())
    t2 = asyncio.create_task(make_request())

    await t1
    await t2


asyncio.run(main())
