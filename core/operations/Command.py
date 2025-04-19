from abc import ABC, abstractmethod

# defining a command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

