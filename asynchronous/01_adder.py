import asyncio


def add_one(number: int) -> int:
    return number + 1


async def add_one_co(number: int) -> int:
    return number + 1


result = add_one(5)
coroutine_result = add_one_co(5)

print(f"normal function result: {result} and type is: {type(result)}")
print(f"coroutine result: {coroutine_result} and type is: {type(coroutine_result)}")

# OUTPUT:
# normal function result: 6 and type is: <class 'int'>
# coroutine result: <coroutine object add_one_co at 0x72e135c9b640> and type is: <class 'coroutine'>


# Notice how when we call our normal add_one function it executes immediately and returns what we would expect,
# another integer. However, when we call coroutine_ add_one we don’t get our code in the coroutine executed at all.
# We get a coroutine object instead. This is an important point, as coroutines aren’t executed when we call them
# directly. Instead, we create a coroutine object that can be run later. To run a coroutine, we need to explicitly run
# it on an event loop. So how can we create an event loop and run our coroutine? In versions of Python older than 3.7,
# we had to create an event loop if one did not already exist. However, the asyncio library has added several functions
# that abstract the event loop management. There is a convenience function, asyncio.run, we can use to run our coroutine

print (f"coroutine result: {asyncio.run(coroutine_result)} and type is: {type(coroutine_result)}")

# OUTPUT:
# coroutine result: 6 and type is: <class 'coroutine'>

# asyncio.run is doing a few important things in this scenario. First, it creates a brand-new event. Once it
# successfully does so, it takes whichever coroutine we pass into it and runs it until it completes, returning the
# result. This function will also do some cleanup of anything that might be left running after the main coroutine
# finishes. Once everything has finished, it shuts down and closes the event loop.
