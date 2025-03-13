import threading

class SharedResource:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            # Critical section: atomic update of value
            self.value = self.value + 1

resource = SharedResource()

def worker(iterations) -> None:
    for _ in range(iterations):
        resource.increment()


threads = []
for _ in range(8):
    t = threading.Thread(target=worker, args=(100000,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final Value: {resource.value}")