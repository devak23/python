# Advanced applications may also involve using specialized libraries that abstract some of the complexity inherent in
# these models. For example, concurrent.futures offers a uniform interface for thread and process pools,
# facilitating a consistent scheduling mechanism across these paradigms. An advanced implementation that combines
# both models is illustrated below:

import concurrent.futures
import time

def cpu_intensive_work(x):
    total = 0
    for i in range(100000):
        total += i * x
    return total

def io_heavy_work(x):
    time.sleep(1)
    return x

def invoke():
    # create a pool of CPU intensive tasks
    with concurrent.futures.ProcessPoolExecutor() as process_executor:
        process_results = list(process_executor.map(cpu_intensive_work, range(10)))

    # create a pool of I/O bound tasks
    with concurrent.futures.ThreadPoolExecutor() as thread_executor:
        thread_results = list(thread_executor.map(io_heavy_work, range(10)))

    print(f"CPU bound results: {process_results}")
    print(f"IO bound results: {thread_results}")


if __name__ == '__main__':
    invoke()

# This example demonstrates splitting workloads based on their operational characteristics. The choice among these
# models also reflects on error propagation and exception handling strategies. In asynchronous code, exceptions must be
# propagated through coroutine chains and managed by the event loop, whereas thread-based errors must be captured within
# the context of each thread and communicated through shareddata structures or dedicated logging mechanisms.
# Process-based errors, on the other hand, require careful handling of return codes and may necessitate re-establishing
# state in a parent process when a worker process terminates unexpectedly. Advanced applications systematically
# integrate comprehensive error handling frameworks that unify these disparate models under a common operational semantics.