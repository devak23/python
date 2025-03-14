# Process-based concurrency, implemented via the multiprocessing module, is instrumental when tackling CPU bound tasks
# circumvented by the GIL. Each process has its own independent memory space, allowing true parallel execution on
# multicore systems. This isolation simplifies the management of shared state at the cost of more complex inter process
# communication (IPC) schemes such as queues, pipes, or shared memory segments. Advanced use-cases often demand a
# balanced approach where process pools manage a fluctuating number of worker processes, and communication overhead is
# minimized by partitioning workloads efficiently. Consider the following example that demonstrates a parallel workload
# through a process pool:

import multiprocessing as mp

def compute(data):
    # intensive computation simulated for a loop or algorithm
    result = sum(i * i for i in data)
    return result

def invoke():
    data_chunks = [range(100000), range(100000, 200000), range(200000, 300000)]
    with mp.Pool(processes=8) as pool:
        results = pool.map(compute, data_chunks)
    print(f"Computed results: {results}")

if __name__ == '__main__':
    invoke()


# The example highlights dynamic mapping of tasks to worker processes, a common strategy for parallel execution.
# Advanced practitioners must evaluate trade-offs such as the overhead introduced by process spawning, data
# serialization cost for inter-process messaging, and the proper partitioning of CPU-bound tasks to achieve optimal
# scaling.

# In this paradigm, each spawned process runs in isolation from the others, and thus, the GIL is instantiated
# independently within each process. For advanced practitioners, careful design considerations must include strategies
# for efficient serialization and deserialization of data between processes and for managing shared resources through
# mechanisms such as shared memory or inter-process communication (IPC).


# Each concurrency model comes with intrinsic trade-offs.
# 1. Thread-based concurrency offers lightweight task scheduling and shared memory convenience but is limited by the GIL
# in CPU-bound applications.
# 2. Asynchronous programming excels in maximizing throughput for I/O-bound workloads, although it demands rethinking
# the control flow by embracing a callback- or coroutine-centric design.
# 3. Process-based concurrency sidesteps the GIL entirely, enabling true parallelism at the cost of increased IPC
# complexity and resource consumption.
#
# An integrated architecture might even leverage a hybrid approach: use asynchronous programming to manage high-level
# orchestration and I/O activities, while offloading CPU-intensive tasks to a dedicated process pool.