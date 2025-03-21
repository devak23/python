import asyncio
from util.logging_functions import logger
from util.timing_functions import async_timed

@async_timed()
async def induce_delay(delay_seconds: int) -> int:
    logger.info(f"{__name__} Delaying for {delay_seconds} seconds")
    await asyncio.sleep(delay_seconds)
    logger.info(f"Finished delaying for {delay_seconds} seconds")
    return delay_seconds

async_timed()
async def main():
    task_1 = asyncio.create_task(induce_delay(2))
    task_2 = asyncio.create_task(induce_delay(3))

    await asyncio.gather(task_1, task_2)

if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:
# 2025-03-21 14:02:50,964 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'induce_delay' with args: (2,) and kwargs: {}
# 2025-03-21 14:02:50,964 - [INFO] - [19_timing-decorator.induce_delay]:~  __main__ Delaying for 2 seconds
# 2025-03-21 14:02:50,964 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: Starting 'induce_delay' with args: (3,) and kwargs: {}
# 2025-03-21 14:02:50,964 - [INFO] - [19_timing-decorator.induce_delay]:~  __main__ Delaying for 3 seconds
# 2025-03-21 14:02:52,966 - [INFO] - [19_timing-decorator.induce_delay]:~  Finished delaying for 2 seconds
# 2025-03-21 14:02:52,967 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'induce_delay' took 2.0028 seconds to complete
# 2025-03-21 14:02:53,966 - [INFO] - [19_timing-decorator.induce_delay]:~  Finished delaying for 3 seconds
# 2025-03-21 14:02:53,966 - [INFO] - [timing_functions.wrapped]:~  DECORATOR: 'induce_delay' took 3.0025 seconds to complete