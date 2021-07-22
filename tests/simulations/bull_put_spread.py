from datetime import datetime, timedelta
from options_freedom.pattern.bull_put_spread import BullPutSpread

from options_freedom.conditions.open.vix_range import VIXRange
from options_freedom.conditions.close.max_loss_take_profit import MaxLossTakeProfit


# simulation time period
start = datetime(2006, 1, 4)
end = datetime(2007, 1, 1)
# days for expiration target
expiration_target = timedelta(45)

open_condition = VIXRange(
    lower=0,
    upper=20
    )

close_condition = MaxLossTakeProfit(
    max_loss_percent=100.0,
    take_profit_percent=50.0
    )

pattern = BullPutSpread()

