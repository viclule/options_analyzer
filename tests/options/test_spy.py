from datetime import date, datetime

from options_freedom.option.base import Option, Type
from options_freedom.option.spy import SPY


def test_get_quote():
    spy = SPY()
    spy.load(load_dir="tests/data/options/spy")
    quote = spy.get_quote(
        Option(
            under=spy.symbol.symbol,
            type=Type.P,
            strike=131.0,
            expiration=datetime(2006, 9, 16),
        ),
        datetime(2006, 1, 4, 15),
    )
    assert quote.bid == 6.3
