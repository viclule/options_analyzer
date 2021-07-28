from datetime import datetime, timedelta

from options_freedom.pattern.bull_put_spread import BullPutSpread
from options_freedom.symbol.base import Symbol
from options_freedom.option.spy import spy
from options_freedom.option.base import Type


today = datetime(2006, 1, 4, 15)
# days for expiration target
expiration_target = timedelta(days=45)
# delta for the legs
delta_short_put = 0.30
delta_long_put = 0.15


short_put = spy.get_option(Type.P, today, today + expiration_target, delta_short_put)
long_put = spy.get_option(Type.P, today, today + expiration_target, delta_long_put)

pattern = BullPutSpread(
    symbol=Symbol(symbol="SPY"),
    short=[short_put],
    long=[long_put],
    start_stamp=today
)


def test_properties():
    assert pattern.max_loss == 3.0  # change with comissions
    assert pattern.max_profit == 1.4  # change with comissions
    assert pattern.short[0].expiration == datetime(2006, 2, 18)
    assert pattern.short[0].strike == 125
    assert pattern.long[0].expiration == datetime(2006, 2, 18)
    assert pattern.long[0].strike == 122


def test_price():
    assert pattern.ask(today) == 1.4
    assert pattern.bid(today) == 1.4
    assert pattern.ask(today + timedelta(days=28)) == 0.4
    assert pattern.bid(today + timedelta(days=28)) == 0.4
    assert pattern.ask(pattern.long[0].expiration) == 0.05
    assert pattern.bid(pattern.long[0].expiration) == 0.05
