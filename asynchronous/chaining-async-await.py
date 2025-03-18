import asyncio
from asynchronous import logger

async def get_data():
    await asyncio.sleep(1)
    return "Data"

async def process_data(data):
    await asyncio.sleep(1)
    return data.upper()

async def main():
    data = await get_data()
    processed_data = await process_data(data)
    logger.info(processed_data)

if __name__ == '__main__':
    asyncio.run(main())