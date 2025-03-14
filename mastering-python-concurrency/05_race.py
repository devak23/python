import threading

counter = 0

def unsafe_increment():
    global counter
    counter += 1

threads = [threading.Thread(target=unsafe_increment()) for _ in range(1000)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print (f"Value of counter: {counter}")

# In this example, the lack of synchronization primitives such as locks leads to a non-deterministic final counter value.
# For advanced developers, mitigating race conditions involves implementing atomic operations or using higher-level
# constructs like thread-safe queues and concurrent data structures. Leveraging the atomic module (or implementing
# comparable behavior in Python where possible) can simulate atomic increments, thereby ensuring consistency even
# under highly concurrent updates.