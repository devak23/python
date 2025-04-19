from core.operations.Command import Command


class Division(Command):
    def __init__(self, number1, number2):
        self.number1 = number1
        self.number2 = number2

    def execute(self):
        return self.number1 / self.number2