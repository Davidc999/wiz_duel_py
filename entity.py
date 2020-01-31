from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, hp, name):
        self.hp = hp
        self.name = name
