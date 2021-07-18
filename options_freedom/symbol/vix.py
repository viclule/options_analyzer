from datetime import datetime
from typing import Dict, Text

from options_freedom.symbol.base import SymbolData, Symbol, Quote
from options_freedom.utils import files_in_path


class VIX(SymbolData):
    symbol = Symbol('VIX')

    def load(self):
        adapter = {
            'time_stamp': 'quotedate',
            'bid': 'bid',
            'ask': 'ask'
        }
        return super().load(adapter)

    def get_quote(self, timestamp: datetime) -> Quote:
        return super().get_quote(timestamp)


load_dir = "options_analyzer/options_freedom/data/quotes/vix"

vix = VIX(load_dir)
