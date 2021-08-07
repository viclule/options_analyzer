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
    return os.path.join(dir_path, "results/data/test", filename)


def run():
    # simulation time period
    start = datetime(2006, 1, 1)
    end = datetime(2021, 6, 29)
    vix_limits = [15.0, 20.0, 25.0]
    delta_shorts = [0.3]
    delta_longs = [0.15]
    max_loss_percents = [100.0, 200.0]
    take_profit_percents = [25.0, 50.0, 75.0]

    ix = 0
    for v in vix_limits:
        for d_s in delta_shorts:
            for d_l in delta_longs:
                for m_l in max_loss_percents:
                    for t_p in take_profit_percents:
                        if v == 15.0 and m_l == 100.0:
                            print(f"Skipped the ready ones: v: {v} and m_l: {m_l}")
                            continue
                        ix += 1
                        print(f'#### Start simulation number {ix}, {v}, {d_s}, {d_l}, {m_l}, {t_p} --- {datetime.today()} ###')
                        run_simulation(v, d_s, d_l, m_l, t_p, start, end)
                        print(f'#### Finish simulation number {ix}, {v}, {d_s}, {d_l}, {m_l}, {t_p} ##')


def run_simulation(
        vix_limit: float, delta_short: float, delta_long: float,
        max_loss_percent: float, take_profit_percent: float,
        start: datetime, end: datetime
        ):
    #           strateby_delta_short_delta_long_days_vix_maxloss_takeprofit
    filename = f"BullPutSpread_{str(int(delta_short*100))}_{str(int(delta_long*100))}_45_{str(int(vix_limit))}_{str(int(max_loss_percent))}_{str(int(take_profit_percent))}"
    # days for expiration target
    expiration_target = timedelta(days=45)
    # in case no option for this target is available, this is the max tolerance
    days_tolerance = timedelta(days=15)
    delta_tolerance = 0.1  # 10%
    # delta for the legs
    delta_short_put = delta_short
    delta_long_put = delta_long

    # test in a range
    if vix_limit <= 15.0:
        open_condition = VIXRange(0, upper=vix_limit)
    else:
        open_condition = VIXRange(lower=vix_limit - 5.0, upper=vix_limit)

    close_condition = MaxLossTakeProfit(max_loss_percent=max_loss_percent, take_profit_percent=take_profit_percent)


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
                        print('not viable patter fund')
                        pass
                except Exception as e:
                    # could not find options with the right conditions
                    print('no options found')
                    pass

        # try to close an open trade
        close: bool = False
        if open_trade:
            temp = open_trade.p_l(today)
            print(f'P/L: {temp}, max profit: {open_trade.max_profit}, day: {today}')
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
                    "under_price_close": open_trade.under_price_close,
                    "max_profit": open_trade.max_profit,
                    "max_loss": open_trade.max_loss,
                    "short_strike": open_trade.pattern.short[0].strike,
                    "short_expiration": open_trade.pattern.short[0].expiration,
                    "short_delta": open_trade.pattern._option_data().get_quote(
                        open_trade.pattern.short[0], open_trade.start_stamp
                    ).delta,
                    "long_strike": open_trade.pattern.long[0].strike,
                    "long_expiration": open_trade.pattern.long[0].expiration,
                    "long_delta": open_trade.pattern._option_data().get_quote(
                        open_trade.pattern.long[0], open_trade.start_stamp
                    ).delta
                }
                open_trade = None
                print(f'Closing trade at: {today}, open_trade: {open_trade}')
        if not close or (close and (list(trades.values())[-1].start_stamp == list(trades.values())[-1].finish_stamp)):
            if (close and (trades[today].start_stamp == trades[today].finish_stamp)):
                print('###### THIS WAS SUPER WEIRD! ######')
            # change day only if no trade was closed today
            # since we can open a new one in the same day
            try:
                today = next(gen)
                print(f'Starting a new day: {today}')
            except StopIteration:
                print('Finish of the iteration')
                break
    # persist the results
    with open(gen_results_path(filename), "wb") as f:
        pickle.dump(trades, f)
    with open(gen_results_path(filename + '_ligth'), "wb") as f:
        pickle.dump(trades_light, f)
    print(len(trades))


if __name__ == "__main__":
    run()
