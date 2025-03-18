import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Hello, world!")
    await asyncio.sleep(1)
    logger.info("Goodbye, world!")

asyncio.run(main())

# asyncio.run() creates and runs an event loop executing the main() coroutine. The event loop manages the execution
# of the asyncronous tasks such as asyncio.sleep() and ensures they are executed in the correct order