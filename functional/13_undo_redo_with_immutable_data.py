from typing import List, Tuple


def main() -> None:
    history = create_history()                    # create a history
    history = edit(history, "Hello")        # add a new edit. Result "Hello"
    history = edit(history, "Hello World")  # add another edit. Result "Hello", "Hello World"
    history = undo(history)                       # undo the last edit "Hello World". Result = Hello"
    history = redo(history)                       # redo the last edit "Hello World". Result = "Hello", "Hello World"
    history = undo(history)
    history = undo(history)

    print(history)

def create_history() -> tuple[List[str], int]:
    return [""],0


def edit(history: tuple[List[str], int], value: str) -> tuple[list[str], int]:
    state, current_index = history

    new_state = state[:current_index + 1] + [value]
    return new_state, current_index + 1


def undo(history: tuple[List[str], int]) -> tuple[list[str], int]:
    state, current_index = history
    new_index = max(0, current_index - 1)
    return state, new_index


def redo(history: tuple[List[str], int]) -> tuple[list[str], int]:
    state, current_index = history
    new_index = min(len(state) - 1, current_index + 1)

    return state, new_index


if __name__ == "__main__":
    main()

