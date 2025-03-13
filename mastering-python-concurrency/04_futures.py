# Advanced applications may also involve using specialized libraries that abstract some of the complexity inherent in
# these models. For example, concurrent.futures offers a uniform interface for thread and process pools,
# facilitating a consistent scheduling mechanism across these paradigms. An advanced implementation that combines
# both models is illustrated below:

import concurrent.futures
import time

def cpu_intensive_work(x):
    total = 0
    for i in range(100000):
        total += i
    return total

def io_heavy_work(x):
    time.sleep(1)
    return x

def invoke():
    # create a pool of CPU intensive tasks
    with concurrent.futures.ProcessPoolExecutor as process_executor:
        process_results = list(process_executor.map(cpu_intensive_work, range(10)))

    # create a pool of I/O bound tasks
    with concurrent.futures.ThreadPoolExecutor as thread_executor:
        thread_results = list(thread_executor.map(io_heavy_work, range(10)))

    print("CPU bound")
