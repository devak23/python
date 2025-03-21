# What is a decorator?
# A decorator is a pattern in Python that allows us to add functionality to existing functions without changing that
# function’s code. We can “intercept” a function as it is being called and apply any decorator code we’d like before
# or after that call.

import functools # Provides the `wraps` decorator, which helps preserve the metadata (name, docstring, etc.) of the original function being wrapped.
import time
from .logging_functions import logger
from typing import Callable, Any


def async_timed(): # This is the main decorator function. It doesn’t take any arguments itself
    def wrapper(func: Callable) -> Callable: # - The inner function accepts the original function (`func`) we want to decorate/wrap.
        @functools.wraps(func) # This ensures that the metadata (e.g., name and docstring) of the original `func` is preserved and not replaced by the `wrapped` function.
        # We now create a new coroutine called wrapped. This is a wrapper around our original coroutine that takes its
        # arguments, *args and **kwargs, calls an await statement, and then returns the result.
        async def wrapped(*args, **kwargs) -> Any: # The `*args` and `**kwargs` allow the `wrapped` function to handle any combination of positional and keyword arguments for the original `func`.
            #logger.info(f"DECORATOR: Starting '{func.__name__}' with args: {args} and kwargs: {kwargs}")
            start = time.time()
            try:
                return await func(*args, **kwargs) # invoke the function
            finally:
                end = time.time()
                total = end - start
                logger.info(f"DECORATOR: '{func.__name__}' took {total:.4f} seconds to complete")

        # The `wrapped` function (which now includes the additional logging and timing logic) is returned at the end
        # of `wrapper`. This makes it the new decorated version of the original `func`.
        return wrapped

    return wrapper

