import asyncio
from asynchronous import logger

async def task1():
    logger.info("Starting task1")
    await asyncio.sleep(1)
    return "Task 1 Finished"

async def task2():
    logger.info("Starting task2")
    await asyncio.sleep(1)
    return "Task 2 Finished"

async def main():
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())
    done, pending = await asyncio.wait([t1, t2])
    for task in done:
        logger.info(task.result())


if __name__ == '__main__':
    asyncio.run(main())