from abc import ABC, abstractclassmethod


class OpenCondition(ABC):
    @abstractclassmethod
    def can_open(self) -> bool:
        pass


class CloseCondition(ABC):
    @abstractclassmethod
    def can_close(self) -> bool:
        pass
