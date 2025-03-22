# We can create an event loop by using the asyncio.new_event_loop method. This will return an event loop instance.
# With this, we have access to all the low-level methods that the event loop has to offer. With the event loop we
# have access to a method named run_until_complete, which takes a coroutine and runs it until it finishes. Once we
# are done with our event loop, we need to close it to free any resources it was using. This should normally be in a
# finally block so that any exceptions thrown don’t stop us from closing the loop

import asyncio
from util.logging_functions import logger


async def main():
    await asyncio.sleep(1)


loop = asyncio.new_event_loop()
logger.info(f"Event loop created: {loop}")
try:
    loop.run_until_complete(main())
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    logger.info(f"Closing event loop: {loop}")
    loop.close()

# This is similar to what happens when we call asyncio.run with the difference being that this does not perform
# canceling any remaining tasks. If we want any special cleanup logic, we would do so in our finally clause.
