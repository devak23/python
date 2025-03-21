# In the previous code (20_pitfall-cpu-bound-task) we saw that ins pite of making our functions async and running it
# in two tasks, it took the same time and manner in executing those tasks sequentially. So "make everything async" could be
# a though leading to the possibility of getting the best of both worlds. However, it may degrade the performance especially
# when we have other coroutines or tasks that have "await" expressions.

import asyncio
from util.logging_functions import logger
from util.timing_functions import async_timed
from util.delay_functions import delay

@async_timed()
async def cpu_bound_work() -> int:
    result = 0
    for i in range(10000000):
        result += i
    return result

@async_timed()
async def main():
    task_1 = asyncio.create_task(cpu_bound_work())
    task_2 = asyncio.create_task(cpu_bound_work())
    delay_task = asyncio.create_task(delay(4))

    await asyncio.gather(task_1, task_2, delay_task)

if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT

# 2025-03-21 18:47:39,118 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'main' with args: () and kwargs: {}
# 2025-03-21 18:47:39,118 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'cpu_bound_work' with args: () and kwargs: {}
# 2025-03-21 18:47:39,580 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'cpu_bound_work' took 0.4620 seconds to complete
# 2025-03-21 18:47:39,580 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'cpu_bound_work' with args: () and kwargs: {}
# 2025-03-21 18:47:40,024 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'cpu_bound_work' took 0.4433 seconds to complete
# 2025-03-21 18:47:40,024 - [INFO] - [delay_functions.delay]:~  sleeping for 4 second(s)
# 2025-03-21 18:47:44,027 - [INFO] - [delay_functions.delay]:~  Finished sleeping for 4 second(s)
# 2025-03-21 18:47:44,028 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'main' took 4.9097 seconds to complete


# We might expect to take the same amount of time as in 20_pitfall-cpu-bound-tasks.py After all, won’t delay_task run
# concurrently alongside the CPU-bound work? In this instance it won’t because we create the two CPU-bound tasks first,
# which, in effect, blocks the event loop from running anything else. This means the runtime of our application will be
# the sum of time it took for our two cpu_bound_work tasks to finish plus the 4 seconds that our delay task took.
# If we need to perform CPU-bound work and still want to use async / await syntax, we can do so. To do this we’ll still
# need to use multiprocessing, and we need to tell asyncio to run our tasks in a process pool.