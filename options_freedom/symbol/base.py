import logging

from typing import Text, Dict
from datetime import datetime
from abc import ABC, abstractclassmethod
from dateutil.parser import parse

import pandas as pd
from pydantic import BaseModel

from options_freedom.models.constants import time_stamp
from options_freedom.utils import files_in_path

logger = logging.getLogger(__name__)


class Symbol(BaseModel):
    symbol: Text


class Quote(BaseModel):
    time_stamp: datetime
    bid: float
    ask: float
    bid_ma: float
    ask_ma: float

    @property
    def mid(self):
        return (self.bid + self.ask) / 2

    @property
    def mid_ma(self):
        # middle of the moving average
        return (self.bid_ma + self.ask_ma) / 2


class SymbolData(ABC):

    symbol: Symbol
    load_dir: Text

    @abstractclassmethod
    def load(self, adapter: Dict[Text, Text], rolling: int = 20, hour: int = None):
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
        self._df['bid_ma'] = self._df['bid'].rolling(rolling, min_periods=1).mean()
        self._df['ask_ma'] = self._df['ask'].rolling(rolling, min_periods=1).mean()
        logger.info(f"{self.symbol.symbol} data was loaded!")

    def get_quote(self, timestamp: datetime) -> Quote:
        """extract the closest quote for a timestamp"""
        row = self._df.iloc[self._df[time_stamp].sub(timestamp).abs().idxmin()]
        return Quote(**row.to_dict())
