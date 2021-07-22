from abc import ABC, abstractclassmethod


class Condition(ABC):
    @abstractclassmethod
    def can_open(self) -> bool:
        pass
