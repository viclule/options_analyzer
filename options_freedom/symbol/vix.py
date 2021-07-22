from options_freedom.symbol.base import Symbol, SymbolData
from options_freedom.models.constants import time_stamp


class VIX(SymbolData):
    symbol = Symbol(symbol="VIX")
    load_dir = "options_freedom/data/quotes/vix"

    def load(self):
        adapter = {"Date": time_stamp, "Close": "bid", "Adj Close": "ask"}
        super().load(adapter, hour=15)
