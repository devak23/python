# A future is a Python object that contains a single value that you expect to get at some point in the future but may
# not yet have. Usually, when you create a future, it does not have any value it wraps around because it doesn’t yet
# exist. In this state, it is considered incomplete, unresolved, or simply not done. Then, once you get a result,
# you can set the value of the future. This will complete the future; at that time, we can consider it finished and
# extract the result from the future

from asyncio import Future
from utils.logging_functions import logger


# We can create a future by calling its constructor. At this time, the future will have no result set on it,
# so calling its done method will return False.
my_future = Future()
logger.info(f"Is my future done?: {my_future.done()}. State of my future: {my_future._state}")

my_future.set_result(42)
logger.info(f"Is my future done now?: {my_future.done()}. State of my future now: {my_future._state}")

logger.info(f"What is the result of my future?: {my_future.result()}")

# OUTPUT:
# /home/abhay/Workspace/python/asynchronous/15_future1.py:12: DeprecationWarning: There is no current event loop
#   my_future = Future()
# 2025-03-21 03:59:02,490 - asynchronous - INFO - Is my future done?: False. State of my future: PENDING
# 2025-03-21 03:59:02,490 - asynchronous - INFO - Is my future done now?: True. State of my future now: FINISHED
# 2025-03-21 03:59:02,490 - asynchronous - INFO - What is the result of my future?: 42

# Futures can also be used in await expressions. If we await a future, we’re saying “pause until the future has a
# value set that I can work with, and once I have a value, wake up and let me process it.”
