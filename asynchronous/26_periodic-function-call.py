import asyncio
from datetime import datetime


async def periodic_function():
    # Your periodic task here
    print(f"Periodic task executed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def schedule_periodic_function():
    # Schedule the periodic function to run after 5 minutes
    loop = asyncio.get_running_loop()
    loop.call_later(5 * 60, schedule_periodic_function)  # 5 minutes in seconds
    asyncio.create_task(periodic_function())

async def main():
    # Schedule the first run of the periodic function
    schedule_periodic_function()

    # Keep the event loop running indefinitely
    while True:
        await asyncio.sleep(60)  # Sleep for 60 seconds to keep the event loop running

# Run the main function
asyncio.run(main())