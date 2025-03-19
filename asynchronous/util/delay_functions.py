import asyncio

from .logging_functions import logger


async def delay(delay_seconds: int, message=None) -> int:
    if not message:
        logger.info(f"sleeping for {delay_seconds} second(s)")
    else:
        logger.info(f"{message} sleeping for {delay_seconds} second(s)")
    await asyncio.sleep(delay_seconds)

    if not message:
        logger.info(f"Finished sleeping for {delay_seconds} second(s)")
    else:
        logger.info(f"{message} Finished sleeping for {delay_seconds} second(s)")

    return delay_seconds