from utils.logging_functions import logger
from utils.delay_functions import delay

import asyncio


async def main():
    task = asyncio.create_task(delay(10, "long running task"))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        logger.info(f"Result: {result}")
    except asyncio.exceptions.TimeoutError:
        logger.error("Task is taking longer than 5 seconds to complete. Please hang on, it will complete soon.")
        result = await task
        logger.info(f"Result: {result}")


if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:
# 2025-03-20 01:39:40,034 - asynchronous - INFO - long running task sleeping for 10 second(s)
# 2025-03-20 01:39:45,035 - asynchronous - ERROR - Task is taking longer than 5 seconds to complete. Please hang on, it will complete soon.
# 2025-03-20 01:39:50,035 - asynchronous - INFO - long running task Finished sleeping for 10 second(s)
# 2025-03-20 01:39:50,035 - asynchronous - INFO - Result: 10

# Canceling tasks automatically if they take longer than expected is normally a good idea. Otherwise, we may have a
# coroutine waiting indefinitely, taking up resources that may never be released. However, in certain circumstances
# we may want to keep our coroutine running. For example, we may want to inform a user that something is taking
# longer than expected after a certain amount of time but not cancel the task when the timeout is exceeded.
# To do this we can wrap our task with the asyncio.shield function. This function will prevent cancellation of the
# coroutine we pass in, giving it a “shield,” which cancellation requests then ignore.
