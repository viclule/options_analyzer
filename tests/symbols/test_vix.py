from datetime import datetime

from options_freedom.symbol.vix import VIX


def test_get_quote():
    vix = VIX()
    vix.load()
    quote = vix.get_quote(datetime(2005, 1, 19, 15))
    assert quote.bid == 13.18
    assert quote.bid_ma == 13.26


def test_get_quote_2():
    vix = VIX()
    vix.load()
    quote = vix.get_quote(datetime(2005, 3, 19, 15))
    assert quote.bid == 13.14
    assert quote.bid_ma == 12.4685
