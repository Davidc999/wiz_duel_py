from abc import ABC, abstractmethod

class PlayerBase(ABC):

    @abstractmethod
    def get_move(self):
        pass

    @abstractmethod
    def print(self):
        pass