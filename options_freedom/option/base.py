from typing import Text, Optional, Dict, List
from datetime import datetime, timedelta
from enum import Enum
from abc import ABC, abstractclassmethod
from dateutil.parser import parse

import pandas as pd
from pydantic import BaseModel

from options_freedom.models.constants import time_stamp, expiration, option_columns
from options_freedom.utils import files_in_path
from options_freedom.symbol.base import Symbol


class Type(Enum):
    C = "C"
    P = "P"


class Option(BaseModel):
    under: Text
    type: Type
    strike: float
    expiration: datetime


class OptionQuote(BaseModel):
    time_stamp: datetime
    delta: float
    bid: float
    ask: float
    under_last: Optional[float] = None

    @property
    def mid(self):
        return (self.bid + self.ask) / 2


class OptionData(ABC):

    symbol: Symbol
    load_dir: Text

    @abstractclassmethod
    def load(self, adapter: Dict[Text, Text], hour: int = None, load_dir: Text = None):
        """load the quotes from csv file(s)"""
        if load_dir is None:
            files = files_in_path(self.load_dir)
        else:
            files = files_in_path(load_dir)
        li = []
        for f in files:
            df = pd.read_csv(
                f"{self.load_dir}/{f}",
                usecols=list(adapter.keys()),
            )
            df = df.rename(adapter, axis="columns")
            if hour:
                df[time_stamp] = df[time_stamp].astype(str) + f"-{str(hour)}"
            df[time_stamp] = df[time_stamp].apply(lambda x: parse(x))
            li.append(df)
        self._df = pd.concat(li, axis=0, ignore_index=True)
        self._df["delta"] = self._df["delta"].abs()
        # reduce to the deltas we are interested
        # not reducable
        # self._df = self._df[(0.13 < self._df["delta"]) & (self._df["delta"] < 0.32)]
        self._df = self._df.reset_index(drop=True)

    def get_quote(self, option: Option, timestamp: datetime) -> OptionQuote:
        """extract the closest quote for an option and timestamp"""
        # prefilter for the given option
        option_df = self._df[
            (self._df["under"] == option.under)
            & (self._df["type"] == option.type.value)
            & (self._df["strike"] == option.strike)
            & (self._df["expiration"] == option.expiration.strftime("%Y-%m-%d"))
        ]
        option_df = option_df.reset_index(drop=True)
        # find the quote for the closest timestamp
        row = option_df.iloc[option_df[time_stamp].sub(timestamp).abs().idxmin()]
        return OptionQuote(**row.to_dict())

    def get_option(
        self, type: Type, today: datetime, expiration: datetime, delta: float
    ) -> Option:
        """extract the closest Option for a delta and expiration date"""
        # prefilter for the given expiration
        prefilter_df = self._df[
            (self._df["time_stamp"] == today)
            & (self._df["type"] == type.value)
        ]
        # search in the exact day, and from there outwards
        for day in self._set_search_date(expiration):
            option_df = prefilter_df[
                (prefilter_df["expiration"] == day.strftime("%Y-%m-%d"))
            ]
            if not option_df.empty:
                break
        option_df = option_df.reset_index(drop=True)
        # find the quote for the closest timestamp
        row = option_df.iloc[(abs(option_df['delta']) - delta).abs().argsort()[0]]
        # row = option_df.iloc[option_df["delta"].sub(delta).abs().idxmin()]
        return Option(
            under=row["under"],
            type=Type(row["type"]),
            strike=row["strike"],
            expiration=parse(row["expiration"]),
        )

    def _set_search_date(self, day: datetime) -> List[datetime]:
        """Set of days around the desired one to search

        Args:
            day (datetime): [description]

        Returns:
            List[datetime]: [description]
        """
        days = [day]
        for i in range(1, 6):
            days.append(day + timedelta(days=i))
            days.append(day - timedelta(days=i))
        return days
