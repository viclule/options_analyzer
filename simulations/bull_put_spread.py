from datetime import datetime, timedelta
from typing import Dict
import pickle
import os 

from options_freedom.symbol.base import Symbol
from options_freedom.pattern.bull_put_spread import BullPutSpread
from options_freedom.conditions.open.vix_range import VIXRange
from options_freedom.option.spy import spy
from options_freedom.option.base import Type
from options_freedom.conditions.close.max_loss_take_profit import MaxLossTakeProfit
from options_freedom.simulator.time_flow import TimeFlow
from options_freedom.models.trade import Trade

dir_path = os.path.dirname(os.path.realpath(__file__))

def gen_results_path(filename: str):
    return os.path.join(dir_path, "results/data", filename)


def run():
    #           strateby_delta_short_delta_long_days_vix
    filename = "BullPutSpread_30_15_45_15"
    # simulation time period
    start = datetime(2006, 1, 4)
    end = datetime(2008, 12, 1)
    # days for expiration target
    expiration_target = timedelta(days=45)
    # in case no option for this target is available, this is the max tolerance
    days_tolerance = timedelta(days=15)
    delta_tolerance = 0.1  # 10%
    # delta for the legs
    delta_short_put = 0.30
    delta_long_put = 0.15


    open_condition = VIXRange(lower=0, upper=15)

    close_condition = MaxLossTakeProfit(max_loss_percent=100.0, take_profit_percent=50.0)


    # status variables
    open_trade: Trade = None
    # date it was open, and the trade object
    trades: Dict[datetime, Trade] = {}
    trades_light: Dict[datetime, Dict] = {}

    timeflow = TimeFlow(start, end)
    gen = timeflow.gen()
    today: datetime = next(gen)
    while today:
        # for each day in the period
        if not open_trade:
            # we can try to open a new trade
            if open_condition.can_open(today):
                # find the closest legs for the given delta and expiration time
                try:
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
                    # add it if between tolerance
                    if (pattern.max_duration < expiration_target + days_tolerance) or \
                            (pattern.max_duration > expiration_target - days_tolerance):
                        # open it       
                        trades[today] = trade
                        open_trade: Trade = trade
                        print(f'Opening trade at: {today}')
                    else:
                        # not viable trade
                        pass
                except Exception as e:
                    # could not find options with the right conditions
                    pass

        # try to close an open trade
        close: bool = False
        if open_trade:
            temp = open_trade.p_l(today)
            close = close_condition.can_close(
                open_trade.p_l(today),
                open_trade.max_profit)
            if close or (today.replace(hour=0) == open_trade.pattern.expiration):
                trades[open_trade.start_stamp].finish_stamp = today
                trades[open_trade.start_stamp].under_price_close = open_trade.pattern.under_price(today)
                trades[open_trade.start_stamp].profit_loss = open_trade.p_l(today)
                trades[open_trade.start_stamp].finish_price = open_trade.pattern.bid(today)
                # ligth format
                trades_light[open_trade.start_stamp] = {
                    "start_stamp": open_trade.start_stamp,
                    "finish_stamp": open_trade.finish_stamp,
                    "open_price": open_trade.open_price,
                    "finish_price": open_trade.finish_price,
                    "profit_loss": open_trade.profit_loss,
                    "under_price_open": open_trade.under_price_open,
                    "under_price_close": open_trade.under_price_close
                }
                open_trade = None
                print(f'Closing trade at: {today}')
        if not close:
            # change day only if no trade was closed today
            # since we can open a new one in the same day
            try:
                today = next(gen)
            except StopIteration:
                break
    # persist the results
    with open(gen_results_path(filename), "wb") as f:
        pickle.dump(trades, f)
    with open(gen_results_path(filename + '_ligth'), "wb") as f:
        pickle.dump(trades_light, f)
    print(len(trades))


if __name__ == "__main__":
    run()
