def partition(arr, low, high) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(array, low, high) -> None:
    if low < high:
        pi = partition(array, low, high)
        quick_sort(array, low, pi - 1)
        quick_sort(array, pi+1, high)



if __name__ == '__main__':
    numbers = [3, 5, 1, 28, 4, 2]
    quick_sort(numbers, 0, len(numbers)-1)
    print(numbers)