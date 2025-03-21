import aiohttp
import asyncio
from util.logging_functions import logger


async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        return f"Error fetching data from {url}: {e}"


async def main():
    urls = ['http://www.example.com/', 'http://www.example.com/', 'http://api.example.com/2']

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Task {i} raised an exception: {result}")
            else:
                logger.info(f"Result -----------{i}--------------------:")
                logger.info(result)


if __name__ == '__main__':
    asyncio.run(main())