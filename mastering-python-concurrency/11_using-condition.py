# The threading module is one of the oldest concurrency frameworks in Python and is designed for high-level
# management of threads operating within the same process. Threads in Python share the same memory space, which
# both simplifies data exchange and increases the risk of race conditions if careful synchronization is not enforced.
# Advanced usage of threading involves not only leveraging intrinsic locks, conditions, and semaphores, but also
# designing custom synchronization primitives when working with non-trivial shared resources. Frameworks built
# atop threading typically incorporate reentrant locks for recursive function calls or adopt patterns that efficiently
# handle thread lifecycle management. The following example demonstrates a more complex coordination scenario
# among multiple threads, implementing a barrier for controlled task synchronization

import threading

# The `ReusableBarrier` class uses `threading.Condition` to synchronize multiple threads (e.g. workers).
# The main task of the `ReusableBarrier` is to block all threads at a certain point (the barrier) until
# enough threads (determined by the number of "parties") have reached it.
class ReusableBarrier:
    def __init__(self, parties):
        self.parties = parties
        self.count = 0
        self.condition = threading.Condition()

    # Lock management:
    # The `Condition` ensures that updates to the shared variable `count` are atomic.
    # This is done using the `with self.condition:` context when modifying `self.count`.
    def attempt(self):
        with self.condition:
            self.count += 1  # Each thread increments `self.count` when it reaches the barrier

            # Waiting and Signalling: If the `self.count` indicates that all required parties (i.e., number of workers)
            # are present, the barrier is reset (`self.count = 0`) and `self.condition.notify_all()` is called.
            # This releases all waiting threads to continue execution.
            if self.count == self.parties:
                self.count = 0

                # When shared state is updated `condition.notify()` wakes up one waiting thread. `condition.notify_all()`
                # wakes up all waiting threads.
                self.condition.notify_all()


# All threads are started in the main, and each calls the `worker` function.
# Each thread executes:
# Incrementing the counter (`self.count`) inside `ReusableBarrier.attempt()` under `Condition` protection.
# If the current thread is not the last one to reach the barrier, it will wait (implicitly synchronized by the `Condition`).
# The last thread to reach the barrier signals all other threads to proceed using `self.condition.notify_all()`.
def worker(barrier, id):
    print(f"Worker {id} before barrier")
    # When each thread executes `barrier.attempt()`, it checks whether it should wait (`self.count < self.parties`)
    # or release other threads (`count == parties`).
    barrier.attempt()
    print(f"Worker {id} after barrier")

def main():
    num_workers = 4
    barrier = ReusableBarrier(num_workers)
    threads = [threading.Thread(target=worker, args=(barrier, i)) for i in range(num_workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()