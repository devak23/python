import asyncio
from asyncio import CancelledError

from utils.logging_functions import logger
from utils.delay_functions import delay


async def main():
    long_task = asyncio.create_task(delay(10, "long running task"))
    seconds_elapsed = 0

    while not long_task.done():
        logger.info("Task is not finished. Checking again in a second")
        await asyncio.sleep(1)
        seconds_elapsed +=1
        if seconds_elapsed == 5:
            long_task.cancel()

    try:
        await long_task
    except CancelledError:
        logger.warning("Our long running task was cancelled!")

if __name__ == '__main__':
    asyncio.run(main())