
from options_freedom.pattern.bull_put_spread import BullPutSpread
from options_freedom.conditions.close.max_loss_take_profit import MaxLossTakeProfit
from options_freedom.symbol.base import Symbol
from options_freedom.strategy.base import Strategy
from options_freedom.conditions.open.vix_range import VIXRange


class SPYBullPut45Days(Strategy):
    pass


def build_strategy():
    spy_bull_put_45_days = SPYBullPut45Days(
        symbol=Symbol(symbol="SPY"),
        open_condition=VIXRange(
            lower=0,
            upper=20
        ),
        close_condition=MaxLossTakeProfit(
            max_loss_percent=100.0,
            take_profit_percent=50.0
        )
        pattern=BullPutSpread
    )
