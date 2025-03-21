# We may also be tempted to use our existing libraries for I/O-bound operations by wrapping them in coroutines.
# However, this will generate the same issues that we saw with CPU-bound operations. These APIs block the main
# thread. Therefore, when we run a blocking API call inside a coroutine, we’re blocking the event loop thread itself,
# meaning that we stop any other coroutines or tasks from executing. Examples of blocking API calls include libraries
# such as requests, or time.sleep. Generally, any function that performs I/O that is not a coroutine or performs
# time-consuming CPU operations can be considered blocking.


import asyncio
import requests
from util.timing_functions import async_timed

@async_timed()
async def get_example_status() -> int:
    response = requests.get("http://www.example.com")
    return response.status_code

@async_timed()
async def main():
    task_1 = asyncio.create_task(get_example_status())
    task_2 = asyncio.create_task(get_example_status())
    task_3 = asyncio.create_task(get_example_status())

    await asyncio.gather(task_1, task_2, task_3)

if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:

# 2025-03-21 19:29:35,561 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'main' with args: () and kwargs: {}
# 2025-03-21 19:29:35,561 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'get_example_status' with args: () and kwargs: {}
# 2025-03-21 19:29:45,600 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'get_example_status' took 10.0382 seconds to complete
# 2025-03-21 19:29:45,600 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'get_example_status' with args: () and kwargs: {}
# 2025-03-21 19:29:53,736 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'get_example_status' took 8.1355 seconds to complete
# 2025-03-21 19:29:53,736 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'get_example_status' with args: () and kwargs: {}
# 2025-03-21 19:29:53,779 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'get_example_status' took 0.0433 seconds to complete
# 2025-03-21 19:29:53,779 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'main' took 18.2181 seconds to complete

# This shows we didn't get any benefits of concurrency. This is again because the requests library is blocking, meaning
# it will block whichever thread it is run on. Since asyncio only has one thread, the requests library blocks the event
# loop from doing anything concurrently.
#
# As a rule, most APIs you employ now are blocking and won’t work out of the box with asyncio. You need to use a library
# that supports coroutines and utilizes non-blocking sockets. This means that if the library you are using does not
# return coroutines, and you aren’t using await in your own coroutines, you’re likely making a blocking call.
#
# In the above example we can use a library such as aiohttp, which uses non-blocking sockets and returns coroutines to
# get proper concurrency. This is shown in 23_blocking-api-correct-way.py