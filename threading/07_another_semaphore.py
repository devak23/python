# importing the modules
import time
from threading import *

# creating thread instance where count = 3
my_obj = Semaphore(4)


# creating instance
def show(the_name):
    # calling acquire method
    my_obj.acquire()
    for n in range(6):
        print(f'Javatpoint, ')
        time.sleep(1)
        print(the_name)

        # calling release method
        my_obj.release()

# creating multiple thread
thread_1 = Thread(target=show, args=('Thread 1',))
thread_2 = Thread(target=show, args=('Thread 2',))
thread_3 = Thread(target=show, args=('Thread 3',))
thread_4 = Thread(target=show, args=('Thread 4',))
thread_5 = Thread(target=show, args=('Thread 5',))
thread_6 = Thread(target=show, args=('Thread 6',))

# calling the threads
thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()
thread_5.start()
thread_6.start()