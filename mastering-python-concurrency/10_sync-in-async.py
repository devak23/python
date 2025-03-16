# Performance considerations in event-driven programming center on the efficient management of the event loop and
# minimizing blocking code. Insertions of synchronous operations in an asynchronous context can lead to detrimental
# delays. When unavoidable, advanced developers offload such operations using executors that run them in separate
# threads or processes, thereby preventing blockage of the event loop. This technique is implemented through the
# loop.run_in_executor() method, which bridges the gap between blocking code and asynchronous flows.

import asyncio
import time


def blocking_io() -> str:
    time.sleep(2)
    return "I/O completed"


async def non_blocking_io(id) -> str:
    await asyncio.sleep(0.5)
    return f"Processed data-{id}"


async def main() -> None:
    await invoke_async_tasks()
    await invoke_sync_tasks()


async def invoke_async_tasks():
    tasks = [asyncio.create_task(non_blocking_io(i)) for i in range(10)]
    completed, pending = await asyncio.wait(tasks, timeout=1.0)

    for task in completed:
        print(f"{task.result()}")

    for task in pending:
        print(f"cancelling {task.get_name()}")
        task.cancel()


async def invoke_sync_tasks():
    loop = asyncio.get_running_loop()
    sync_result = await loop.run_in_executor(None, blocking_io)
    print(sync_result)


if __name__ == '__main__':
    asyncio.run(main())

# This example shows how we can integrate legacy blocking code into an asynchronous system without compromising the
# performance of the event loop. In high-performance applications, judicious use of executors minimizes latency and
# maximizes parallel throughput, ensuring that blocking operations do not lead to bottlenecks. Advanced event-driven
# architectures also focus on reducing overhead by optimizing the granularity of asynchronous tasks. Instead of
# creating a multitude of micro-tasks, which might overwhelm the event loop with scheduling overhead, developers are
# advised to batch operations when possible. Batching reduces the frequency of context switches and allows the event
# loop to process groups of events efficiently. Furthermore, the use of efficient data structures for task management
# and event queuing can enhance performance. Techniques such as leveraging lock free queues (where applicable in an
# asynchronous context) and minimizing memory allocations contribute significantly to improving throughput.
