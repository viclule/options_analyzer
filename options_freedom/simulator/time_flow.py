"""Defines a set of time where conditions can be assessed.
For example:
All the instants between 1.1.2010 to 1.1.2012 where the market was
opened at 10:45am
"""
from datetime import datetime

from options_freedom.option.spy import spy
from options_freedom.models.constants import time_stamp

market_days = sorted(list(set(spy._df[time_stamp].tolist())))


class TimeFlow:
    def __init__(self, start: datetime, end: datetime):
        self.set = [day for day in market_days if day >= start and day <= end]

    def gen(self) -> datetime:
        """Next market open day in the sequence.

        Returns:
            datetime: [description]
        """
        for day in self.set:
            yield day

    def reset(self):
        pass
