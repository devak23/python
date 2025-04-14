# When seeing the performance improvements we can obtain from running some of our longer tasks concurrently,
# we can be tempted to start to use coroutines and tasks everywhere in our applications. While it depends on the
# application you’re writing, simply marking functions async and wrapping them in tasks may not help application
# performance. In certain cases, this may degrade performance of your applications.
#
# Two main errors occur when trying to turn your applications asynchronous.
# 1. Attempting to run CPU-bound code in tasks or coroutines without using multiprocessing;
# 2. Using blocking I/O-bound APIs without using multithreading.

# Let's take a look at CPU bound code running in a coroutine
import asyncio
from utils.timing_functions import async_timed

# We may have functions that perform computationally expensive calculations, such as looping over a large dictionary
# or doing a mathematical computation. Where we have several of these functions with the potential to run
# concurrently, we may get the idea to run them in separate tasks. In concept, this is a good idea, but remember that
# asyncio has a single-threaded concurrency model. This means we are still subject to the limitations of a single
# thread and the global interpreter lock.

@async_timed()
async def cpu_bound_task() -> int:
    counter = 0
    for _ in range(10000000):
        counter += 1
    return counter

@async_timed()
async def main():
    task_1 = asyncio.create_task(cpu_bound_task())
    task_2 = asyncio.create_task(cpu_bound_task())
    await asyncio.gather(task_1, task_2)

if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:

# 2025-03-21 18:37:28,792 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'main' with args: () and kwargs: {}
# 2025-03-21 18:37:28,792 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'cpu_bound_task' with args: () and kwargs: {}
# 2025-03-21 18:37:29,186 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'cpu_bound_task' took 0.3939 seconds to complete
# 2025-03-21 18:37:29,186 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'cpu_bound_task' with args: () and kwargs: {}
# 2025-03-21 18:37:29,571 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'cpu_bound_task' took 0.3846 seconds to complete
# 2025-03-21 18:37:29,571 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'main' took 0.7789 seconds to complete

# We see that, despite creating two tasks, our code still executes sequentially. First, we run Task 1, then we run Task 2,
# meaning our total runtime will be the sum of the two calls to cpu_bound_work. Now we may be tempted to think that there
# are no drawbacks to making all our code use async and await. After all, it ends up taking the same amount of time as if
# we had run things sequentially. However, by doing this we can run into situations where our application’s performance
# can degrade. This is depicted in 21_pitfall-cpu-bound-task.
