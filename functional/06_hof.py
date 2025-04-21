def double(x: int) -> int:
    return x * 2

def apply_func(func: callable, x: int) -> callable:
    return func(x)


print(apply_func(double, 4))

# what does the order mean? (in Higher order functions)
# Order means the rank or the level of a function based on the complexity of its operations on other functions.
# 1st order: functions on basic data types: int, str, ...
# higher order: operate on functions themselves (taking them as inputs or returning them)