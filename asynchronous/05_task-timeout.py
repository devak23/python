import asyncio
from util.logging_functions import logger
from util.delay_functions import delay


async def main():
    delay_task = asyncio.create_task(delay(4, message='Long running task'))
    try:
        result = await asyncio.wait_for(delay_task, timeout=3)
        logger.info(f"Task completed with result: {result}")
    except asyncio.exceptions.TimeoutError:
        logger.error(f"Task: {delay_task} timed out")
        logger.info(f"Was the task cancelled? {delay_task.cancelled()}")


if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:
# 2025-03-20 01:11:03,118 - asynchronous - INFO - Long running task sleeping for 4 second(s)
# 2025-03-20 01:11:06,120 - asynchronous - ERROR - Task timed out
# 2025-03-20 01:11:06,121 - asynchronous - INFO - Was the task cancelled? True


# Checking every second or at some other time interval, and then canceling a task, as we did in the previous example,
# isn’t the easiest way to handle a timeout. Ideally, we’d have a helper function that would allow us to specify this
# timeout and handle cancellation for us.
