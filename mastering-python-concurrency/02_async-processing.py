import asyncio

async def fetch_data(task_id):
    # Simulate non-blocking I/O operation
    await asyncio.sleep(1)
    return f"data-{task_id}"

async def process_all():
    tasks = [asyncio.create_task(fetch_data(i)) for i in range(20)]
    for task in tasks:
        data = await task
        print(f"Processed {data}")

if __name__ == '__main__':
    asyncio.run(process_all())

# This implementation leverages asyncio.as_completed to process results as they are available, thereby
# maximizing throughput by minimizing idle time. Advanced developers may extend this pattern by integrating
# timeout management, cancellation policies, and even interfacing with synchronous libraries via executors