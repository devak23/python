import asyncio

async def task1():
    print("Task 1")
    await asyncio.sleep(1)
    print("Task 1 done")

async def task2():
    print("Task 2")
    await asyncio.sleep(0.5)
    print("Task 2 done")

async def main():
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())
    await t1
    await t2

if __name__ == '__main__':
    asyncio.run(main())
