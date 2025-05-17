from multiprocessing import Pool
from os import cpu_count
from functools import partial
from typing import List


def calc_power(y: int, x: int) -> int:
    return x ** y


def process_list(comparison_list: List[int]) -> List[int]:
    print(f"cpu count: {cpu_count()}")
    num_cpus_to_be_used = max(1, cpu_count() - 1)

    power = 3

    partial_function = partial(calc_power, power)

    with Pool(num_cpus_to_be_used) as pool:
        result = pool.map(partial_function, comparison_list)

    return result


if __name__ == '__main__':
    comparison_list = [i for i in range(1, 5)]
    result = process_list(comparison_list)
    print(result)