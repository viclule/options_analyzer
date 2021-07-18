"""Defines a set of time where conditions can be assessed.
For example:
All the instants between 1.1.2010 to 1.1.2012 where the market was
opened at 10:45am
"""
from datetime import datetime


class TimeFlow:
    def __init__(self, start: datetime, end: datetime, time: datetime):
        pass

    def next(self) -> datetime:
        """Next time in the sequence.

        Returns:
            datetime: [description]
        """
        pass

    def reset(self):
        pass
