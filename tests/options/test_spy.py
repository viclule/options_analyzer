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
    # on the exact day
    option = spy.get_option(Type.P, datetime(2006, 1, 4, 15), datetime(2006, 9, 16), 0.28)
    assert option.expiration == datetime(2006, 9, 16)
    assert option.strike == 122.0


def test_get_option():
    # the closest day
    option = spy.get_option(Type.P, datetime(2006, 1, 4, 15), datetime(2006, 9, 15), 0.28)
    assert option.expiration == datetime(2006, 9, 16)
    assert option.strike == 122.0


def test_get_option_2():
    # the closest day
    option = spy.get_option(Type.P, datetime(2006, 1, 11, 15), datetime(2006, 2, 25), 0.28)
    assert option.expiration == datetime(2006, 2, 18)
    assert option.strike == 127.0


def test_get_option_3():
    # the closest day
    option = spy.get_option(Type.P, datetime(2006, 2, 16, 15), datetime(2006, 4, 2), 0.3)
    assert option.expiration == datetime(2006, 3, 18)
    assert option.strike == 127.0
