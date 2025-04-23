# given a dictionary with string keys and integer values, the task is to write a function that transforms the dict
# based on the following criteria

# 1. The keys in the new dict should be in reverse order of the original keys
# 2. The values in the new dict should be increased by 10

p = lambda x: print(x)

data = {
    'abc': 5,
    'def': 10,
    'ghi': 15,
}

reverse_add = lambda key,val: (key[::-1], val + 10)

new_data = dict(map(reverse_add, data.keys(), data.values()))

p(new_data)

################### Another implementation ###################

reverse_add2 = lambda item: (item[0][::-1], item[1] + 10)
new_data2 = map(reverse_add2, data.items())
p(dict(new_data2))