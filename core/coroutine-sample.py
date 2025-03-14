# A **coroutine** is a special kind of function in Python that allows for asynchronous programming. Unlike a regular
# function, which is executed from start to finish in a single sequence, a coroutine can pause its execution
# (i.e., suspend itself) and resume later. This makes it particularly useful for handling tasks that involve waiting
# (such as I/O operations) without blocking the program.

import asyncio
import random

async def download_file(f) -> None:
    print(f"started downloading: {f}...")
    await asyncio.sleep(random.randint(1,10)) # Simulating download delay
    print(f"finished downloading: {f}")

async def main() -> None:
    # Run coroutines concurrently
    await asyncio.gather(
        download_file("file1.txt"),
        download_file("file1.txt"),
        download_file("file1.txt")
    )

if __name__ == '__main__':
    asyncio.run(main())

# OUTPUT:
# started downloading: file1.txt...
# started downloading: file1.txt...
# started downloading: file1.txt...
# finished downloading: file1.txt
# finished downloading: file1.txt
# finished downloading: file1.txt
# Each `download_file` coroutine is executed concurrently. The event loop ensures that tasks don’t block each other,
# waiting for the I/O operations to complete.

# - Is a function defined with `async def`.
# - Uses `await` to pause and resume execution at specific points.
# - Is non-blocking and works with asynchronous tasks effectively.
# - Depends on an event loop for its execution.
