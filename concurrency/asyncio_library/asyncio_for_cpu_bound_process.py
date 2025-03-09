import asyncio
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
async def factorial(number):
    n = number
    i = 2
    while i < number:
       n *= i
       i += 1
    return n

@async_timed()
async def main():
    t1 = asyncio.create_task(factorial(55555))
    t2 = asyncio.create_task(factorial(55555))

    await t1
    await t2


asyncio.run(main())
