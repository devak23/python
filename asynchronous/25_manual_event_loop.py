import asyncio
from util.logging_functions import logger
from util.delay_functions import delay


def future_func():
    logger.info("I am called in the future")


async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(future_func)
    await delay(1)


if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT

# 2025-03-21 21:08:24,043 - [INFO] - [delay_functions.delay]:~  sleeping for 1 second(s)
# 2025-03-21 21:08:24,043 - [INFO] - [25_manual_event_loop.future_func]:~  I am called in the future
# 2025-03-21 21:08:25,044 - [INFO] - [delay_functions.delay]:~  Finished sleeping for 1 second(s)

# our main coroutine gets the event loop with asyncio.get _running_loop and tells it to run call_soon, which takes a
# function and will run it on the next iteration of the event loop. In addition, there is an asyncio.get_event_loop
# function that lets you access the event loop. This function can potentially create a new event loop if it is called
# when one is not already running, leading to strange behavior. It is recommended to use get_running_loop,
# as this will throw an exception if an event loop isn’t running, avoiding any surprises.
#
# While we shouldn’t use the event loop frequently in our applications, there are times when we will need to
# configure settings on the event loop or use low-level functions
