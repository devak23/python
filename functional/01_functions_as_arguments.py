def greet() -> str:
    return "Hello!"

print(greet())

def shout(f) -> str:
    return f() + "!!!"

print(shout(greet)) # we are passing a reference to the greet function. We are not invoking it. We are just passing the
# pointer to the function greet which gets invoked inside the shout function