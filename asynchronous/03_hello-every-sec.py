import asyncio
from utils.logging_functions import logger
from utils.delay_functions import delay

async def hello_every_sec():
    for i in range(2):
        await asyncio.sleep(1)
        logger.info("I'm running other code while I'm waiting ")

async def main():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_sec()
    await first_delay
    await second_delay

if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:
# sleeping for 3 seconds(s)
# sleeping for 3 seconds(s)
# 2025-03-20 00:41:49,831 - asynchronous - INFO - I'm running other code while I'm waiting
# 2025-03-20 00:41:50,832 - asynchronous - INFO - I'm running other code while I'm waiting
# Finished sleeping for 3 second(s)
# Finished sleeping for 3 second(s)

# First, we start two tasks that sleep for 3 seconds; then, while our two tasks are idle, we start to see I’m running
# other code while I’m waiting! being printed every second. This means that even when we’re running time-intensive
# operations, our application can still be performing other tasks.

# One potential issue with tasks is that they can take an indefinite amount of time to complete. We could find ourselves
# wanting to stop a task if it takes too long to finish. Tasks support this use case by allowing cancellation.