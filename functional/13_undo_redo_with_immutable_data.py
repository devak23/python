from typing import List, Tuple

# The idea behind the undo, redo and edit is that the underlying data storage (list, array, db... whatever)  will ALWAYS
# maintain ALL the values that were added to it. The undo is only illusory which is managed by index pointing up to a
# specific element in the data structure. If things are "undone" by the client, the actual data isn't dropped in the
# the underlying data structure. In this following implementation, the "current_state" shows the "virutal end" of the list
# not the real one. This is managed by actively updating the pointer to the "alleged last element" in the list.

def main() -> None:
    history = create_history()                    # create a history
    print(current_state(history))
    history = edit(history, "Hello")        # add a new edit. Result "Hello"
    print(current_state(history))
    history = edit(history, "Hello World")  # add another edit. Result "Hello", "Hello World"
    print(current_state(history))
    history = undo(history)                       # undo the last edit "Hello World". Result = Hello"
    print(current_state(history))
    history = redo(history)                       # redo the last edit "Hello World". Result = "Hello", "Hello World"
    print(current_state(history))
    history = undo(history)
    print(current_state(history))
    history = undo(history)
    print(current_state(history))


# Gives the element from the list at the "latest index" internally maintained.
def current_state(history) -> tuple[List[str], int]:
    state, current_index = history
    return state[current_index], current_index

# creates a simple list with nothing in it and the pointer index pointing to the zeroth element
def create_history() -> tuple[List[str], int]:
    return [""],0

# this will update the internal list with the value added and increment the pointer to point to it
def edit(history: tuple[List[str], int], value: str) -> tuple[list[str], int]:
    state, current_index = history

    new_state = state[:current_index + 1] + [value]
    return new_state, current_index + 1

# the undo will simply decrement the pointer by one and will NOT actually pop the element off the list.
def undo(history: tuple[List[str], int]) -> tuple[list[str], int]:
    state, current_index = history
    new_index = max(0, current_index - 1)
    return state, new_index

# again, this will simply increment the pointer by one, the data remaining the same.
def redo(history: tuple[List[str], int]) -> tuple[list[str], int]:
    state, current_index = history
    new_index = min(len(state) - 1, current_index + 1)

    return state, new_index


if __name__ == "__main__":
    main()

