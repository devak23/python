import asyncio
from utils.logging_functions import logger
from utils.timing_functions import async_timed

@async_timed()
async def induce_delay(delay_seconds: int) -> int:
    logger.info(f"{__name__} Delaying for {delay_seconds} seconds")
    await asyncio.sleep(delay_seconds)
    logger.info(f"Finished delaying for {delay_seconds} seconds")
    return delay_seconds

@async_timed()
async def main():
    task_1 = asyncio.create_task(induce_delay(2))
    task_2 = asyncio.create_task(induce_delay(3))

    await asyncio.gather(task_1, task_2)

if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:
# 2025-03-21 14:33:40,982 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'main' with args: () and kwargs: {}
# 2025-03-21 14:33:40,982 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'induce_delay' with args: (2,) and kwargs: {}
# 2025-03-21 14:33:40,982 - [INFO] - [19_timing-decorator.induce_delay]:~  __main__ Delaying for 2 seconds
# 2025-03-21 14:33:40,983 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'induce_delay' with args: (3,) and kwargs: {}
# 2025-03-21 14:33:40,983 - [INFO] - [19_timing-decorator.induce_delay]:~  __main__ Delaying for 3 seconds
# 2025-03-21 14:33:42,985 - [INFO] - [19_timing-decorator.induce_delay]:~  Finished delaying for 2 seconds
# 2025-03-21 14:33:42,985 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'induce_delay' took 2.0028 seconds to complete
# 2025-03-21 14:33:43,984 - [INFO] - [19_timing-decorator.induce_delay]:~  Finished delaying for 3 seconds
# 2025-03-21 14:33:43,984 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'induce_delay' took 3.0017 seconds to complete
# 2025-03-21 14:33:43,985 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'main' took 3.0022 seconds to complete


# We can see that our two delay calls were both started and finished in roughly 2 and 3 seconds, respectively, for a
# total of 5 seconds. Notice, however, that our main coroutine only took 3 seconds to complete because we were waiting
# concurrently.