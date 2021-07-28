from datetime import datetime, timedelta
from typing import Dict


from options_freedom.symbol.base import Symbol
from options_freedom.pattern.bull_put_spread import BullPutSpread
from options_freedom.conditions.open.vix_range import VIXRange
from options_freedom.option.spy import spy
from options_freedom.option.base import Type
from options_freedom.conditions.close.max_loss_take_profit import MaxLossTakeProfit
from options_freedom.simulator.time_flow import TimeFlow
from options_freedom.models.trade import Trade


# simulation time period
start = datetime(2006, 1, 4)
end = datetime(2007, 1, 1)
# days for expiration target
expiration_target = timedelta(45)
# delta for the legs
delta_short_put = 0.30
delta_long_put = 0.15


open_condition = VIXRange(lower=0, upper=20)

close_condition = MaxLossTakeProfit(max_loss_percent=100.0, take_profit_percent=50.0)

pattern = BullPutSpread()

# status variables
open_trade: Trade = None
# date it was open, and the trade object
trades: Dict[datetime, Trade] = {}

timeflow = TimeFlow(start, end)
today = timeflow.next()
while today:
    # for each day in the period
    if not open_trade:
        # we can try to open a new trade
        if open_condition.can_open(today):
            # find the closest legs for the given delta and expiration time
            short_put = spy.get_option(
                Type.P,
                today,
                today + timedelta(days=expiration_target),
                delta_short_put,
            )
            long_put = spy.get_option(
                Type.P, today, today + timedelta(days=expiration_target), delta_long_put
            )
            pattern = BullPutSpread(
                symbol=Symbol(symbol="SPY"),
                short=[short_put],
                long=[long_put],
            )
            # open it
            trade = Trade(
                pattern=pattern,
                stat_result=today,
                max_loss=pattern.max_loss(),
                max_profit=pattern.price(today),
                open_price=pattern.price(today),
            )
            # add it
            trades[today] = trade
            open_trade: Trade = trade

    # try to close an open trade
    if open_trade:
        close = close_condition.can_close(open_trade.p_l(today), open_trade.max_profit)
        if close:
            trades[open_trade.start_stamp].finish_stamp = today
            trades[open_trade.start_stamp].profit_loss = open_trade.p_l(today)
            open_trade = None
    today = timeflow.next()
