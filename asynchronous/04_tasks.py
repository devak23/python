import asyncio
from utils.logging_functions import logger
from utils.delay_functions import delay


async def task1():
    logger.info("Task 1")
    await asyncio.sleep(1)
    logger.info("Task 1 done")

async def task2():
    logger.info("Task 2")
    await asyncio.sleep(1)
    logger.info("Task 2 done")

async def main():
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())
    t3 = asyncio.create_task(delay(1))
    logger.info(f"type of t3 = {type(t3)}")
    await t1
    await t2
    result = await t3
    logger.info(f"returned {result} from t3")

if __name__ == '__main__':
    asyncio.run(main())

# It is important to know that we should usually use an await keyword on our tasks at some point in our application.
# If we did not use await, our task would be scheduled to run, but it would almost immediately be stopped and
# “cleaned up” when asyncio.run shuts down the event loop. Using await on our tasks in our application also has
# implications for how exceptions are handled.

# Each call to create_task returns instantly, so we reach the await statement right away. Tasks are scheduled to run
# “as soon as possible.” Generally, this means the first time we hit an await statement after creating a task, any
# tasks that are pending will run as await triggers an iteration of the event loop.

# Since we’ve hit await for all 3 tasks, they start running and will carry out any sleep operations concurrently. This
# means that the program will complete in about 3 seconds. If we were to run these delay operations sequentially,
# we’d have an application runtime of just over 9 seconds. By doing this concurrently, we’ve decreased the total runtime
# of this application three-fold!