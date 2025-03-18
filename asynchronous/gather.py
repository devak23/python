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
    tasks = [task1(), task2()]
    results = await asyncio.gather(*tasks)
    logger.info(results)

if __name__ == '__main__':
    asyncio.run(main())