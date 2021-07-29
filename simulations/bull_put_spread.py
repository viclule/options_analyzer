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


def run():
    # simulation time period
    start = datetime(2006, 1, 4)
    end = datetime(2006, 4, 1)
    # days for expiration target
    expiration_target = timedelta(45)
    # delta for the legs
    delta_short_put = 0.30
    delta_long_put = 0.15


    open_condition = VIXRange(lower=0, upper=20)

    close_condition = MaxLossTakeProfit(max_loss_percent=100.0, take_profit_percent=50.0)


    # status variables
    open_trade: Trade = None
    # date it was open, and the trade object
    trades: Dict[datetime, Trade] = {}

    timeflow = TimeFlow(start, end)
    gen = timeflow.next()
    today = next(gen)
    while today:
        # for each day in the period
        if not open_trade:
            # we can try to open a new trade
            if open_condition.can_open(today):
                # find the closest legs for the given delta and expiration time
                short_put = spy.get_option(
                    Type.P,
                    today,
                    today + expiration_target,
                    delta_short_put,
                )
                long_put = spy.get_option(
                    Type.P,
                    today,
                    today + expiration_target,
                    delta_long_put
                )
                pattern = BullPutSpread(
                    symbol=Symbol(symbol="SPY"),
                    short=[short_put],
                    long=[long_put],
                    start_stamp=today,
                    expiration=short_put.expiration
                )
                # open it
                trade = Trade(
                    pattern=pattern,
                    start_stamp=today,
                    max_loss=pattern.max_loss,
                    max_profit=pattern.ask(today),
                    open_price=pattern.ask(today),
                    under_price_open=pattern.under_price(today)
                )
                # add it
                trades[today] = trade
                open_trade: Trade = trade

        # try to close an open trade
        close: bool = False
        if open_trade:
            temp = open_trade.p_l(today)
            close = close_condition.can_close(
                open_trade.p_l(today),
                open_trade.max_profit)
            if close:
                trades[open_trade.start_stamp].finish_stamp = today
                trades[open_trade.start_stamp].under_price_close = open_trade.pattern.under_price(today)
                trades[open_trade.start_stamp].profit_loss = open_trade.p_l(today)
                open_trade = None
        if not close:
            # change day only if no trade was closed today
            # since we can open a new one in the same day
            try:
                today = next(gen)
            except StopIteration:
                break

    print(len(trades))


if __name__ == "__main__":
    run()
