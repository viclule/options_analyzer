from os import stat_result
from typing import Text, Optional, Dict, List, Tuple
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
        self._dfs = {}
        for ix, f in enumerate(files):
            df: pd.DataFrame = pd.read_csv(
                f"{self.load_dir}/{f}",
                usecols=list(adapter.keys()),
            )
            df = df.rename(adapter, axis="columns")
            if hour:
                df[time_stamp] = df[time_stamp].astype(str) + f"-{str(hour)}"
            df[time_stamp] = df[time_stamp].apply(lambda x: parse(x))
            df["delta"] = df["delta"].abs()
            (year, month) = __class__._get_year_month_from_filename(f)
            print(f'Loading option file {ix}, from {len(files)}')
            try:
                self._dfs[year][month] = df
            except KeyError:
                self._dfs[year] = {}
                self._dfs[year][month] = df

    def get_quote(self, option: Option, timestamp: datetime) -> OptionQuote:
        """extract the closest quote for an option and timestamp"""
        # prefilter for the given option
        option_df = self._dfs[timestamp.year][timestamp.month][
            (self._dfs[timestamp.year][timestamp.month]["under"] == option.under)
            & (self._dfs[timestamp.year][timestamp.month]["type"] == option.type.value)
            & (self._dfs[timestamp.year][timestamp.month]["strike"] == option.strike)
            & (self._dfs[timestamp.year][timestamp.month]["expiration"] == option.expiration.strftime("%Y-%m-%d"))
        ]
        option_df = option_df.reset_index(drop=True)
        # find the quote for the closest timestamp
        row = option_df.iloc[option_df[time_stamp].sub(timestamp).abs().idxmin()]
        return OptionQuote(**row.to_dict())

    def get_option(
        self, type: Type, today: datetime, expiration: datetime, delta: float, exact_expiration_date: bool = False
    ) -> Option:
        """extract the closest Option for a delta and expiration date"""
        # prefilter for the given expiration
        prefilter_df = self._dfs[today.year][today.month][
            (self._dfs[today.year][today.month]["time_stamp"] == today)
            & (self._dfs[today.year][today.month]["type"] == type.value)
        ]
        # search in the exact day, and from there outwards
        for day in self._set_search_date(expiration, exact_expiration_date=exact_expiration_date):
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

    def _set_search_date(self, day: datetime, exact_expiration_date: bool = False) -> List[datetime]:
        """Set of days around the desired one to search

        Args:
            day (datetime): [description]

        Returns:
            List[datetime]: [description]
        """
        days = [day]
        if exact_expiration_date:
            return days
        for i in range(1, 20):
            days.append(day + timedelta(days=i))
            days.append(day - timedelta(days=i))
        return days

    @staticmethod
    def _get_year_month_from_filename(filename: Text) -> Tuple[int, int]:
        """Extracts year and month from string. Ex:
        UnderlyingOptionsEODCalcs_2015-06.csv

        Args:
            filename (Text): [description]
        """
        text = filename.split('_')[1].split('.')[0]
        return int(text[0:4]), int(text[5:7])
