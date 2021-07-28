from datetime import datetime

from options_freedom.option.base import Option, Type
from options_freedom.option.spy import spy


def test_get_quote():
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


def test_get_option():
    option = spy.get_option(Type.P, datetime(2006, 1, 4, 15), datetime(2006, 9, 16), 0.28)
    assert option.expiration == datetime(2006, 9, 16)
    assert option.strike == 122.0
