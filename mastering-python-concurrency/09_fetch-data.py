import asyncio

async def fetch_data(id) -> str:
    await asyncio.sleep(0.2)
    return f"data-{id}"


async def process_tasks() -> None:
    # Create a list of 100000 asynchronous tasks - each calling fetch_data with an identifier from 0 to 9.
    # `asyncio.create_task(fetch_data(i))` : Wraps the coroutine `fetch_data(i)` into a Task, which is managed by the
    # event loop and runs concurrently

    tasks = [asyncio.create_task(fetch_data(i)) for i in range(100000)]

    # # The `asyncio.wait` function is used to wait for the group of tasks to complete. The wait time is only 1 second
    # for the entire list of tasks, whatever is processed will be displayed
    completed, pending = await asyncio.wait(tasks, timeout=1.0)
    for task in completed:
        try:
            result = task.result()
            print(f"Processed: {result}")
        except Exception as e:
            print(f"Error: {e} encountered during task execution: {task}")

    # Since there are a lot of tasks to be executed, some won't be completed, and we will cancel the pending tasks
    for task in pending:
        print(f"cancelling task: {task.get_name()}")
        task.cancel()

if __name__ == '__main__':
    asyncio.run(process_tasks())

# This type of code is commonly used for tasks like making multiple HTTP requests, reading files asynchronously, or
# querying databases concurrently where high performance and quick response times are critical. It also illustrates how
# tasks can be managed concurrently with precise control over timeouts, providing resilience under variable I/O
# conditions. Advanced usage often involves integrating cancellation and timeout policies, where tasks are organized
# into dependency graphs and subject to dynamic priorities. Such patterns require developers to reason rigorously about
# the state of multiple, interdependent asynchronous components.