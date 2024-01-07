import time
from threading import Thread, Condition


class FrequentTimer:
    """
    If a thread is going to repeatedly signal an event, there is a better object to use: Condition. Here is a code
    that can monitor to see whenever the timer expires.
    """

    def __init__(self, interval: int) -> None:
        self._interval = interval
        self._flag = 0
        self._cv = Condition()

    def start(self) -> None:
        t = Thread(target=self.run)
        t.daemon = True
        t.start()

    def run(self) -> None:
        while True:
            time.sleep(self._interval)
            with self._cv:
                self._flag ^= 1
                self._cv.notify_all()

    def wait_for_tick(self) -> None:
        while self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()


class Counter:
    def __init__(self, target):
        self._ft = FrequentTimer(target)

    def countdown(self, ticks) -> None:
        while ticks > 0:
            self._ft.wait_for_tick()
            print(f'T minus {ticks}')
            ticks -= 1

    def countup(self, last) -> None:
        n = 0
        while n < last:
            self._ft.wait_for_tick()
            print(f'Counting - {n}')
            n += 1


if __name__ == '__main__':
    print('Main thread started')
    c = Counter(5)
    Thread(target=c.countdown, args=(10,)).start()
    Thread(target=c.countup, args=(5,)).start()
    print('Main thread completed')
