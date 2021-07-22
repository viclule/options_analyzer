from typing import Text, Dict
from datetime import datetime
from abc import ABC, abstractclassmethod
from dateutil.parser import parse

import pandas as pd
from pydantic import BaseModel

from options_freedom.models.constants import time_stamp, symbol_columns
from options_freedom.utils import files_in_path


class Symbol(BaseModel):
    symbol: Text


class Quote(BaseModel):
    time_stamp: datetime
    bid: float
    ask: float


class SymbolData(ABC):

    symbol: Symbol
    load_dir: Text

    @abstractclassmethod
    def load(self, adapter: Dict[Text, Text], hour: int = None):
        """load the quotes from csv file(s)"""
        files = files_in_path(self.load_dir)
        li = []
        for f in files:
            df = pd.read_csv(
                f"{self.load_dir}/{f}",
                encoding="ISO-8859-1",
                engine="c",
                usecols=list(adapter.keys()),
            )
            df = df.rename(adapter, axis="columns")
            if hour:
                df[time_stamp] = df[time_stamp].astype(str) + f"-{str(hour)}"
            df[time_stamp] = df[time_stamp].apply(lambda x: parse(x))
            li.append(df)
        self._df = pd.concat(li, axis=0, ignore_index=True)
        self._df = self._df.reset_index(drop=True)

    def get_quote(self, timestamp: datetime) -> Quote:
        """extract the closest quote for a timestamp"""
        row = self._df.iloc[self._df[time_stamp].sub(timestamp).abs().idxmin()]
        return Quote(**row.to_dict())
