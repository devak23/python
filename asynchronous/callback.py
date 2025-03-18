import asyncio
from asynchronous import logger


async def task1():
    await asyncio.sleep(1)
    return "Task 1 Completed"


def callback(task):
    try:
        result = task.result()
        logger.info(f"Callback function called with result: {result}")
    except Exception as e:
        logger.error(f"Task raised an exception: {e}")


async def main():
    task = asyncio.create_task(task1())
    task.add_done_callback(callback)
    await task


if __name__ == '__main__':
    asyncio.run(main())
