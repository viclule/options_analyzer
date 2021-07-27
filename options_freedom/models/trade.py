from typing import Optional

from pydantic import BaseModel
from datetime import datetime, timedelta

from options_freedom.pattern.base import Pattern


class Trade(BaseModel):
    pattern: Pattern
    start_stamp: datetime
    max_loss: float
    max_profit: float
    open_price: float
    # this two can be added after closing the trade
    finish_stamp: Optional[datetime]
    finish_price: Optional[float]
    profit_loss: Optional[float]

    @property
    def length(self) -> timedelta:
        return self.finish_stamp - self.start_stamp

    def p_l(self, timestamp: datetime) -> float:
        return self.open_price - self.pattern.price(timestamp)
