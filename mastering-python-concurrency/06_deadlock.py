import time
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()


def thread1():
    with lock_a:
        time.sleep(0.1)
        with lock_b:
            print("Thread 1 compelted its work")


def thread2():
    with lock_b:
        time.sleep(0.1)
        with lock_a:
            print("Thread 2 compelted its work")


t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)

t1.start()
t2.start()
t1.join()
t2.join()

# In this scenario, thread1 holds lock_a and waits for lock_b while thread2 holds lock_b and waits for lock_a.
# Synchronization is essential for ensuring that concurrent threads or processes coordinate correctly when accessing
# shared resources. Traditional synchronization constructs such as locks, semaphores, and condition variables must be
# employed judiciously. However, over-reliance on these primitives can lead to performance bottlenecks, particularly
# when the contention is high. Advanced methods such as lock-free programming and non-blocking algorithms offer
# alternatives that avoid the overhead of mutual exclusion
