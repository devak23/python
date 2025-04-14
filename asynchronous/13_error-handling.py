import asyncio
from utils.logging_functions import logger


async def async_function():
    try:
        logger.info("Starting async_function")
        await asyncio.sleep(1)
        raise Exception("Something went wrong")
    except Exception as e:
        logger.error(f"async_function raised an exception: {e}")

asyncio.run(async_function())