from core.operations.Command import Command


class Square(Command):
    def __init__(self, number1, number2):
        self._n1 = number1


    def execute(self):
        return self._n1 * self._n1