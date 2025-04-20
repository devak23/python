def outer(x: int) -> callable:
    def inner(y: int) -> int:
        return x * y    # the body of the inner function has access to the variables defined in the outer function

    return inner


multiply_by_4 = outer(4)

result = multiply_by_4(3)

print(result)

# Output:
# 12
