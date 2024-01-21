import numpy as np

arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(f"arr[1:5] = {arr[1:5]}")  # prints [1 2 3 4]. The result includes the start index, but excludes the end index.
print(f"arr[4:] = {arr[4:]}")  # prints [4 5 6 7 8 9]. Starting from index = 4, select all the remaining elements
print(f"arr[:4] = {arr[:4]}")  # prints [0 1 2 3] The result excludes the end index.
print(f"arr[:,] = {arr[:, ]}")  # prints all the elements of the array
print(f"arr[-1] = {arr[-1]}")  # prints the last element of the array = 9

print(f"arr[-3:-1] = {arr[-3:-1]}")
# prints [7 8]. -3 indicates go to the third element in the reverse direction and then go down 2 elements forward
# Again note that the -1 index is excluded.

print(f"arr[::2] = {arr[::2]}")  # prints [0 2 4 6 8]. Returns every 2nd element of the array starting with 0 index
print(f"arr[::3] = {arr[::3]}")  # prints [0 3 6 9]. Returns every 3rd element of the array starting with 0 index

print(f"arr[3::] = {arr[3::]}")  # prints [3 4 5 6 7 8 9]. Returns all elements of the array starting from index 3
print(f"arr[1:5:2] = {arr[1:5:2]}")  # prints [1 3]. Go from index = 1 to 5 (5 excluded) and select the 2nd element

arr = np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']])
print(f"arr[1, 1:4] = {arr[1, 1:4]}")  # prints ['b' 'c' 'd'] as it takes the array at the index=1 and selects elements
# from index=1 to index=3. 4 is excluded as always
print(f"arr[0:2, 2] = {arr[0:2, 2]}")  # prints ['2' 'c'] as it took elements from both the arrays at index=2
print(f"arr[0:3, 2:4] = {arr[0:3, 2:4]}")  # prints [['2' '3'] ['c' 'd']]. The 3 in the 0:3 carries no meaning here
# because there are 2 arrays within the array. if there were a 3rd array, we should have gotten 3 arrays in the
# output. Let's try it out

arr = np.array([[[[2, 4, 6, 8, 10, 12, 14], [1, 3, 5, 7, 9, 11, 13], [99, 88, 77, 66, 55, 44, 33],
                  [-2, -3, -5, -7, -11, -13, -17]]]])
# here we have an array of 4 arrays. Let's see what arr[0:3, 2:4] returns
print(f"arr[2, 2:4] = {arr[2, 2:4]}")
