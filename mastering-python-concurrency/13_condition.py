import threading
import time
import random

def write_data():
    condition.acquire()
    with open('report.txt', 'w+') as f:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday']
        for day in days:
            f.writelines(f'{random.randint(20, 40)}\n')

    condition.notify_all()
    condition.release()

def max_temp():
    condition.acquire()
    condition.wait(timeout=0)
    with open('report.txt', 'r') as f:
        data = f.readlines()
        max = float(data[0].strip("\n"))
        for temp in data:
            if float(temp.strip("\n")) > max:
                max = float(temp.strip("\n"))
        print(f'Max temp is {max}')
    condition.release()

def avg_temp():
    condition.acquire()
    condition.wait(timeout=0)
    with open('report.txt', 'r') as f:
        data = f.readlines()
        total = 0
        for temp in data:
            total += float(temp.strip("\n"))
        avg = total / len(data)
        print(f'Avg temp is {avg}')
    condition.release()

condition = threading.Condition()

t1 = threading.Thread(target=write_data)
t2 = threading.Thread(target=max_temp)
t3 = threading.Thread(target=avg_temp)

t1.start()
t2.start()
t3.start()