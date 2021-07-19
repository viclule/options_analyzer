from datetime import datetime

from options_freedom.symbol.vix import VIX


def test_get_quote():
    vix = VIX()
    vix.load()
    quote = vix.get_quote(datetime(2005, 1, 19, 15))
    assert quote == 13.18
