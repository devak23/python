import asyncio
import time
from utils.logging_functions import logger



async def main():
    start_time = time.time()
    await asyncio.sleep(1)
    end_time = time.time()
    logger.info(f"Sleep took: {end_time - start_time} seconds")


if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:
# 2025-03-21 13:16:14,263 - asynchronous - INFO - Sleep took: 1.00144362449646 seconds

# However, this will get messy quickly when we have multiple await statements and tasks to keep track of. A better
# approach is to come up with a reusable way to keep track of how long any coroutine takes to finish. We can do this
# by creating a decorator that will run an await statement for us. Please check timing_functions for the decorator
# details and 19_timing-decorator for its usage.
