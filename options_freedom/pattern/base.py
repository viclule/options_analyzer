from datetime import datetime
from typing import List, Tuple

from pydantic import BaseModel

from options_freedom.symbol.base import Symbol
from options_freedom.option.base import Option, OptionData, OptionQuote
from options_freedom.option.spy import spy


class Pattern(BaseModel):
    symbol: Symbol
    commissions: float
    short: List[Option]
    long: List[Option]
    start_stamp: datetime

    def ask(self, timestamp: datetime) -> float:
        """The price at the moment. Ask

        Args:
            timestamp (datetime): [description]
            ask (bool, optional): [description]. Defaults to False.

        Returns:
            float: [description]
        """
        (shorts, longs) = self._get_quotes(timestamp)
        return sum(q.bid for q in shorts) + sum(q.ask for q in longs)

    def bid(self, timestamp: datetime) -> float:
        """The price at the moment. Bid

        Args:
            timestamp (datetime): [description]
            ask (bool, optional): [description]. Defaults to False.

        Returns:
            float: [description]
        """
        (shorts, longs) = self._get_quotes(timestamp)
        return sum(q.ask for q in shorts) + sum(q.bid for q in longs)

    @property
    def max_loss(self):
        # to be implemented by the pattern
        pass

    @property
    def max_profit(self):
        return self.ask(self.start_stamp) - self.commissions

    def _get_quotes(self, timestamp) -> Tuple[List[OptionQuote], List[OptionQuote]]:
        short_quotes = [
            self._option_data().get_quote(short, timestamp) for short in self.short
        ]
        long_quotes = [
            self._option_data().get_quote(long, timestamp) for long in self.long
        ]
        return short_quotes, long_quotes

    def _option_data(self) -> OptionData:
        if self.symbol == Symbol(symbol="SPY"):
            return spy
        else:
            raise ValueError("Symbol not supported yet.")
