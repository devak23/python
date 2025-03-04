from typing import List


def insertion_sort(numbers) -> List[int]:
    for i in range(1, len(numbers)):
        # will be used for comparison with previous items, and sent to the place it belongs
        value_at_i = numbers[i]

        # since we want to swap an item with previous one, we start from 1
        index = i

        # we now check the value of each element from the index to the end of the list (ignoring the first one)
        # if the value of element pointed by index happens to be more than value at the initial index i
        while index >= 0 and numbers[index] > value_at_i :
            # we copy the value of pointed by the previous index and place it in the location pointed by the index
            numbers[index] = numbers[index - 1]
            # we continue doing that operation for all the values pointed by the index, ofcourse decrementing the index
            index -= 1

        numbers[index] = value_at_i

    return numbers


def main():
    unsorted_numbers = [10, 21, 1, 4, 89, 2, 7, 22, 12]
    sorted_numbers = insertion_sort(unsorted_numbers)
    print(f'sorted_numbers = {sorted_numbers}')


if __name__ == "__main__":
    main()
