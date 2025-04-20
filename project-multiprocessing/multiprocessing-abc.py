import time
from multiprocessing import Queue, Process


def check_value_in_list(comparison_list, i, number_of_processes, queue):
    max_number_to_check_to = 10**8
    lower_bound = int(i * max_number_to_check_to / number_of_processes)
    upper_bound = int((i + 1) * max_number_to_check_to / number_of_processes)
    number_of_hits = 0

    for i in range(lower_bound, upper_bound):
        if i in comparison_list:
            number_of_hits += 1

    queue.put((lower_bound, upper_bound, number_of_hits))


def main():
    number_of_processes = 4
    comparison_list = [1021, 2345, 3, 5000]
    queue = Queue()

    start = time.time()
    processes = []

    for i in range(number_of_processes):
        p = Process(target=check_value_in_list, args=(comparison_list, i, number_of_processes, queue))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    queue.put("DONE")

    while True:
        v = queue.get()
        if v == "DONE":
            break
        lower_bound, upper_bound, number_of_hits = v
        print(f"lower_bound={lower_bound}, upper_bound={upper_bound}, number_of_hits={number_of_hits}")


    print(f"Time taken: {time.time() - start}")

if __name__ == '__main__':
    main()