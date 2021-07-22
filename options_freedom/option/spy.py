from typing import Text
import sys

from options_freedom.option.base import OptionData
from options_freedom.symbol.base import Symbol
from options_freedom.models.constants import time_stamp


class SPY(OptionData):
    symbol = Symbol(symbol="SPY")
    load_dir = "options_freedom/data/options/spy"

    def load(self, load_dir: Text = None):
        adapter = {
            "quote_date": time_stamp,
            "option_type": "type",
            "strike": "strike",
            "expiration": "expiration",
            "delta_1545": "delta",
            "bid_1545": "bid",
            "ask_1545": "ask",
            "underlying_bid_1545": "under_last",
            "underlying_symbol": "under",
        }
        super().load(adapter, hour=15, load_dir=load_dir)


spy = SPY()
if "pytest" in sys.modules:
    # this is a test
    spy.load(load_dir="tests/data/options/spy")
else:
    spy.load()
