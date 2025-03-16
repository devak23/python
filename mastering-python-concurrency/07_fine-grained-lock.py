import threading
from collections import defaultdict

class SharedDict:
    def __init__(self, num_shards=8):
        self.num_shards = num_shards
        self.shards = [defaultdict(int) for _ in range(num_shards)]
        self.locks = [threading.Lock() for _ in range(num_shards)]

    def _get_shard(self, key):
        return hash(key) % self.num_shards

    def increment(self, key):
        shard = self._get_shard(key)
        with self.locks[shard]:
            self.shards[shard][key] += 1

    def get(self, key):
        shard = self._get_shard(key)
        with self.locks[shard]:
            return self.shards[shard].get(key, 0)

sd = SharedDict()

def worker():
    for i in range(100000):
        sd.increment('item')

threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads:
    t.start()

for t in threads:
    t.join()

print(f"Sharded counter: {sd.get('item')}")


# By dividing the workload across multiple locks, contention is reduced and overall performance is improved. Advanced
# implementers must analyze access patterns to determine the optimal granularity; too coarse-grained a locking scheme
# can serialize execution, while too fine-grained can complicate state management and increase overhead.