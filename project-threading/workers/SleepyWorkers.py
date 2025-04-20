import threading
import time

class SleepyWorkers(threading.Thread):
    def __init__(self, seconds, **kwargs):
        self._seconds = seconds
        super(SleepyWorkers, self).__init__()
        self.start()

    def _sleep_a_little(self):
        time.sleep(self._seconds)

    def run(self):
        self._sleep_a_little()