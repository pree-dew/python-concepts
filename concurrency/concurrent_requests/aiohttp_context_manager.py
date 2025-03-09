import aiohttp
import asyncio
import logging

# Set up logging to see connection activities
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("aiohttp.client")

async def fetch_data(url, session, session_id):
    # Use an existing session passed as parameter
    async with session.get(url) as response:
        logger.info(f"Session {session_id}: Connected to {url}")
        return await response.json()

async def main():
    # Create a single session for all requests
    connector = aiohttp.TCPConnector(limit=1) # Connector
    async with aiohttp.ClientSession(connector=connector) as session:
        # Print connector information before requests
        connector = session._connector
        print(f"Initial connections: {len(connector._conns)}")
        
        # Make multiple requests to the same host to encourage connection reuse
        urls = [
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://jsonplaceholder.typicode.com/posts/2',
            'https://jsonplaceholder.typicode.com/posts/3',
            'https://jsonplaceholder.typicode.com/posts/3',
        ]
        
        # Run first batch sequentially to observe connections
        print("First batch:")
        tasks = [fetch_data(url, session, 1) for url in urls]
        results = await asyncio.gather(*tasks)
        
        # Wait a bit but keep connections alive
        await asyncio.sleep(1)
        print(f"Active connections: {len(connector._conns)}")
        print(f"Connection keys: {list(connector._conns.keys())}")

				 # Run second batch to see if connections are reused
        print("\nSecond batch (should reuse connections):")
        tasks = [fetch_data(url, session, 1) for url in urls]
        results = await asyncio.gather(*tasks)
        
if __name__ == "__main__":
    asyncio.run(main())

