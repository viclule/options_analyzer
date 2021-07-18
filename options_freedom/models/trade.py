from pydantic import BaseModel
from datetime import datetime, timedelta


class Trade(BaseModel):
    start_stamp: datetime
    finish_stamp: datetime
    profit_loss: float
    max_possible_loss: float
    max_possible_profit: float

    @property
    def length(self) -> timedelta:
        return self.finish_stamp - self.start_stamp
