import threading
import time


class HelloThread(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.__message = 'Hello World'

    def run(self) -> None:
        print(f'{self.__message}')

if __name__ == '__main__':
    print('Main thread started')
    t = HelloThread()
    t.start()
    time.sleep(1)
    print('Main thread completed')