# write a program to reverse the arguments of the function given this:
def subtract(x:int, y:int) -> int:
    return x - y

def reverse_args(f: callable) -> callable:
    def wrapper(x: int, y: int) -> callable:
        return f(y,x)

    return wrapper

print(subtract(10, 5))

reverse_subtract = reverse_args(subtract)
print(reverse_subtract(10, 5))

#----------------------- reversing a list---------------
numbers = [1, 2, 3, 4, 5]
print(f"reversed numbers: {numbers[::-1]}")

#----------------------- reversing a list---------------

def reverse_args2(f: callable) -> callable:
    def wrapper(*args, **kwargs) -> callable:
        # Reverse the positional arguments and pass them to the function
        reversed_args = args[::-1]

        # Any keyword arguments (`**kwargs`) are forwarded to the original function without modification.
        return f(*reversed_args, **kwargs)

    return wrapper

# Wrap the function with reverse_args
reverse_subtract2 = reverse_args2(subtract)


print(reverse_subtract2(10, 5))

# Output:
# 5
# -5
# reversed numbers: [5, 4, 3, 2, 1]
# -5