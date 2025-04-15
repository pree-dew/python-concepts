import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial

def sum(n):
    output = 1
    for i in range(1, n + 1):
        output += i
    return n, output

async def main():
    start = time.time()
    with ProcessPoolExecutor() as executor:
        numbers = [100000000, 50000000]
        # Using partial to pass the function and its arguments
        calls = [partial(sum, n) for n in numbers]

        event_loop = asyncio.get_event_loop()
        tasks = []
        for call in calls:
            tasks.append(event_loop.run_in_executor(executor, call))

        for t in asyncio.as_completed(tasks):
            result = await t
            print("Result: {0} = {1}".format(result[0], result[1]))

    print("Time taken = {0:.5f}".format(time.time() - start))

if __name__ == '__main__':
    asyncio.run(main())
