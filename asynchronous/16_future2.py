import asyncio
from asyncio import Future
from util.logging_functions import logger


async def make_request() -> Future:
    future = Future()
    asyncio.create_task(set_future_value(future))
    return future


async def set_future_value(future: Future) -> None:
    await asyncio.sleep(1)
    future.set_result(42)


async def main():
    future = await make_request()  # It is important to use 'await' here as the coroutine will not return a Future
    # but a coroutine itself.

    # When calling an `async` function like `make_request`, you need to either:
    # 1. Await it: to execute the coroutine and obtain its result, e.g., `future = await make_request()`; or
    # 2. Schedule it into the event loop using `asyncio.create_task`, but only if you want it to run as a
    # background task and do not need its immediate result.

    logger.info(f"is the future done? {future.done()}")
    logger.info(f"awaiting the future...")
    value = await future
    logger.info(f"is the future done now? {future.done()}")
    logger.info(f"the future value is {value}")


if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:
# 2025-03-21 03:51:32,271 - asynchronous - INFO - is the future done? False
# 2025-03-21 03:51:32,271 - asynchronous - INFO - awaiting the future...
# 2025-03-21 03:51:33,273 - asynchronous - INFO - is the future done now? True
# 2025-03-21 03:51:33,273 - asynchronous - INFO - the future value is 42

#  we define a function make_request. In that function we create a future and create a task that will asynchronously
#  set the result of the future after 1 second. Then, in the main function, we call make_request. When we call this,
#  we’ll instantly get a future with no result; it is, therefore, undone. Then, we await the future. Awaiting this
#  future will pause main for 1 second while we wait for the value of the future to be set. Once this completes,
#  value will be 42 and the future is done.


# There is a strong relationship between tasks and futures. In fact, task directly inherits from future. A future can
# be thought as representing a value that we won’t have for a while. A task can be thought as a combination of both a
# coroutine and a future. When we create a task, we are creating an empty future and running the coroutine. Then,
# when the coroutine has completed with either an exception or a result, we set the result or exception, of the future.

# Given the relationship between futures and tasks, there is a similar relationship between tasks and coroutines.
# After all, all these types can be used in await expressions. The common thread between these, is the "Awaitable"
# abstract base class. This class defines one abstract double underscore method __await__ and anything that implements
# the __await__ method can be used in an await expression.
#
# Coroutines inherit directly from Awaitable, as do futures. Tasks then extend futures,
#                             ..----------------------------------------:.
#                             .:=                                      ::.
#                             .:=              Awaitable               ::.
#                             .:=                                      ::.
#                              ..-------------------=-------------------..
#                                                  :-.
#                                                  :-.
#                                                  :-.
#                    -------------------------------=:-----------------------------
#                    .-                                                          -:.
#                    .-                                                          -:.
#                   .-#:                                                        .*=.
# .--------------------+-------------------:.                 .-------------------:+=-------------------.
# =                                        =                  .::                                     ::.
# =                Coroutine               =                  .::            Future                   ::.
# =                                        =                  .::                                     ::.
# ----------------------------------------:-                  .-----------------------------------------.
#                                                                                -.
#                                                                                -.
#                                                                               :#=.
#                                                            .-------------------:+=-------------------.
#                                                            ::                                      ::.
#                                                            ::               Task                   ::.
#                                                            ::                                      ::.
#                                                            :---------------------------------------::.
