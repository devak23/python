import asyncio

async def task1():
    await asyncio.sleep(0.2)
    print("Task 1")
    await asyncio.sleep(1)
    print("Task 1 done")

async def task2():
    await asyncio.sleep(0.5)
    print("Task 2")
    await asyncio.sleep(1)
    print("Task 2 done")

async def main():
    await asyncio.gather(task1(), task2())

if __name__ == '__main__':
    asyncio.run(main())

# These two coroutines are executed concurrently using 'asyncio.gather' within the main coroutine. As a result both
# coroutines and their outputs are interleaved demonstrating the concept of concurrency.