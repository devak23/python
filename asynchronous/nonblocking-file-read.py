import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def blocking_read_file(file_name):
    with open(file_name, "r") as f:
        data = f.read()
        logger.info("Blocking: data: ", data)

async def non_blocking_read_file(file_name):
    with open(file_name, "r") as f:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, f.read) # Non-blocking operation
        logger.info("Non-Blocking data: ", data)

if __name__ == '__main__':
    asyncio.run(non_blocking_read_file("../data/purchases.csv"))
    blocking_read_file("../data/purchases.csv")

# asyncio.run_in_executor() allows us to invoke the f.read() (blocking operation) asynchronously without blocking the
# event loop. This enables the program to continue with other tasks while file is being read.