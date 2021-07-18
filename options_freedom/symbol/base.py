from typing import Text, Dict
from datetime import datetime
from abc import ABC, abstractclassmethod
from csv import reader

from pydantic import BaseModel
from pande

from options_freedom.utils import files_in_path


class Symbol(BaseModel):
    symbol: Text


class Quote(Symbol):
    time_stamp: datetime
    bid: float
    ask: float


class SymbolData(ABC):

    symbol: Symbol
    quotes: Dict[datetime, Quote] = []

    def __init__(self, data_path: Text):
        self._data_path = data_path

    @abstractclassmethod
    def load(self, adapter: Dict[Text, Text]):
        """load the quotes from csv file(s)"""
        self.quotes = {}

        files = files_in_path(self._data_path)
        for f in files:
            df
                for row in csv_reader:

                    self.quotes[] = Quote(**args)

    @abstractclassmethod
    def get_quote(self, timestamp: datetime) -> Quote:
        """extrat the closest quote for a timestamp"""
        pass
