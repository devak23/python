from multiprocessing import Pool
from os import cpu_count


def square(x):
    return x ** 2

comparison_list = [i for i in range(1, 100)]
print(f"cpu count: {cpu_count()}")
num_cpus_to_be_used = max(1, cpu_count() - 1)

with Pool(num_cpus_to_be_used) as pool:
    result = pool.map(square, comparison_list)

print(result)
