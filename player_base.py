from abc import ABC, abstractmethod

class PlayerBase(ABC):

    @abstractmethod
    def get_input(self, prompt):
        pass

    @abstractmethod
    def print(self, prompt):
        pass