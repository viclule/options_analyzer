import logging
from datetime import datetime

from options_freedom.conditions.base import OpenCondition
from options_freedom.symbol.vix import vix

logger = logging.getLogger(__name__)


class VIXRange(OpenCondition):
    def __init__(self, lower: float, upper: float):
        if lower < 0 or lower > upper:
            raise ValueError("Unvalid lower value")
        if upper < 0 or upper > 100:
            raise ValueError("Unvalid upper value")
        self._lower = lower
        self._upper = upper

    def can_open(self, time_stamp: datetime) -> bool:
        vix_quote = vix.get_quote(time_stamp)
        if (self._upper > vix_quote.mid > self._lower) and \
                (self._upper > vix_quote.mid_ma > self._lower):
            logger.info("Condition to open satisfied!")
            return True
        return False
