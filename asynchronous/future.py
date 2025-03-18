import asyncio
from asynchronous import logger

async def task1():
    await asyncio.sleep(1)
    return "Task 1 Finished"

async def task2():
    await asyncio.sleep(0.5)
    return "Task 2 Finished"

async def main():
    f1 = asyncio.Future()
    asyncio.create_task(task1()).add_done_callback(f1.set_result)
    await f1
    print(f1.result())


    loop = asyncio.get_running_loop()
    f2 = loop.create_future()
    loop.call_later(0,f2.set_result, "Manually setting result: Task2 is finished!")
    result = await f2
    logger.info(result)
    logger.info(f2.result())

if __name__ == '__main__':
    asyncio.run(main())