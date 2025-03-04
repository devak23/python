from typing import List


def selection_sort(numbers) -> List[int]:
    n = len(numbers)
    for current in range(n):
        # define a "min index" which points to the smaller. Let it be the index of the iteration
        min_idx = current
        # go over the values pointed by next indices assuming the current one is smaller and ...
        for nxt_idx in range(current + 1, n):
            # if then number pointed by next index is less than the number pointed by the "min index"
            if numbers[nxt_idx] < numbers[min_idx]:
                # then min index will be the next index... and repeat this loop for all next indices
                min_idx = nxt_idx
        # assuming you have found the smallest value in the loop above, swap the values of "current min" pointed
        # by current to the newly found "actual min" pointed by min index
        numbers[current], numbers[min_idx] = numbers[min_idx], numbers[current]
    return numbers


def main() -> None:
    unsorted_list = [64,34,25,12,22,11,90]
    sorted_list = selection_sort(unsorted_list)
    print(f'Sorted List = {sorted_list}')

if __name__ == '__main__':
    main()