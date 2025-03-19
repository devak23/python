import asyncio
from util.logging_functions import logger
from util.delay_functions import delay

async def main():
    delay_task = asyncio.create_task(delay(4))
    try:
        result = await asyncio.wait_for(delay_task, timeout=3)
        logger.info(f"Task completed with result: {result}")
    except asyncio.exceptions.TimeoutError:
        logger.error("Task timed out")
        logger.info(f"Was the task cancelled? {delay_task.cancelled()}")

if __name__ == '__main__':
    asyncio.run(main())
