from typing import Text, Dict
from datetime import datetime
from abc import ABC, abstractclassmethod
from csv import reader

import pandas as pd
from pydantic import BaseModel

from options_freedom.models.constants import time_stamp
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
    load_dir: Text

    @abstractclassmethod
    def load(self, adapter: Dict[Text, Text], hour: int = None):
        """load the quotes from csv file(s)"""
        self._df = pd.DataFrame(columns=[time_stamp, 'bid', 'ask'])

        files = files_in_path(self.load_dir)
        for f in files:
            df = pd.read_csv(f'{self.load_dir}/{f}',
                             encoding="ISO-8859-1", engine='c',
                             usecols=['Date', 'Close', 'Adj Close'])
            df = df.rename(adapter, axis='columns')
            time_format = '%Y-%M-%d'
            if hour:
                df[time_stamp] = df[time_stamp].astype(str) + f'-{str(hour)}'
                time_format = '%Y-%M-%d-%H'
            df[time_stamp] = pd.to_datetime(df[time_stamp], format=time_format)
            self._df = self._df.append(df, ignore_index=True)

    def get_quote(self, timestamp: datetime) -> Quote:
        """extrat the closest quote for a timestamp"""
        row = self._df.iloc[self._df[time_stamp].sub(timestamp).abs().idxmin()]
        return row['bid']
