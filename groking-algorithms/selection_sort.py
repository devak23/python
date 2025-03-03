from typing import List


def selection_sort(numbers) -> List[int]:
    n = len(numbers)
    for current in range(n):
        min = current
        for next in range(current + 1, n):
            if numbers[next] < numbers[min]:
                min = next
        numbers[current], numbers[min] = numbers[min], numbers[current]
    return numbers

if __name__ == '__main__':
    unsorted_list = [64,34,25,12,22,11,90]
    sorted_list = selection_sort(unsorted_list)
    print(f'Sorted List = {sorted_list}')