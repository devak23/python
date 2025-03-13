import asyncio
import random

async def handle_request(request_id: int) -> None:
    print(f"Handling request #{request_id}")
    # Simulate an IO bound task using sleep
    await asyncio.sleep(random.randint(1, 5))
    print(f"Completed request #{request_id}")


async def main() -> None:
    # Use gather to run task concurrently
    tasks = [handle_request(i) for i in range(100)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())

# In this example, the event loop schedules multiple handle_request coroutines, each simulating a network call.
# The use of asyncio.gather ensures that all coroutines are executed concurrently while still preserving the
# logical sequential steps within each task. Advanced configurations often require adjusting aspects such as retry
# strategies, connection pooling, and integration with synchronous code using thread executors when computational
# tasks are involved.