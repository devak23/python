from workers.SleepyWorkers import SleepyWorkers
from workers.SquaredSumWorkers import SquaredSumWorkers
import time


def main():
    current_threads = []
    calc_start_time = time.time()
    for i in range(5):
        max_val = (i+1) * 1000000;
        squared_sum_workers = SquaredSumWorkers(n=max_val)
        current_threads.append(squared_sum_workers)

    for t in current_threads:
        t.join()

    print(f"calculate_sum_of_squares took {time.time() - calc_start_time} seconds")

    current_threads = []
    sleep_start_time = time.time()
    for seconds in range(1, 6):
        sleepy_workers = SleepyWorkers(seconds=seconds)
        current_threads.append(sleepy_workers)

    for t in current_threads:
        t.join()

    print(f"sleep_a_little took {time.time() - sleep_start_time} seconds")

if __name__ == "__main__":
    main()