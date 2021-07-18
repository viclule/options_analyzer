from typing import Text, Optional
from datetime import datetime
from enum import Enum
from abc import ABC, abstractclassmethod

from pydantic import BaseModel


class Type(Enum):
    C = "C"
    P = "P"


class Option(BaseModel):
    under: Text
    strike: float
    expiration: datetime
    optionroot: Text
    type_: Type


class OptionQuote(Option):
    time_stamp: datetime
    bid: float
    ask: float
    delta: float
    under_last: Optional[float] = None


class OptionData(ABC):
    def __init__(self, option: Option):
        self._option = option

    @abstractclassmethod
    def load(self, path: Text):
        """load the quotes from a csv file"""
        pass
        self._quotes = []

    @abstractclassmethod
    def get_quote(self, timestamp: datetime) -> OptionQuote:
        """extrat the closest quote for a timestamp"""
        pass
