from datetime import datetime
from typing import List

from options_freedom.strategy.base import Strategy
from options_freedom.models.trade import Trade


class Simulator:
    def __init__(self, strategy: Strategy, start: datetime, end: datetime):
        self._strategy = strategy
        self._start = start
        self._end = end
        self._trades = List[Trade]
        self._ran = False

    def run(self):
        self._ran = True

    @property
    def trades(self):
        if not self._ran:
            raise FirstRunException()
        return self._trades


class FirstRunException(Exception):
    pass
