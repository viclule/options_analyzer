import logging

from options_freedom.conditions.base import Condition
from options_freedom.symbol.vix import vix

logger = logging.getLogger(__name__)


class VIXRange(Condition):
    def __init__(self, lower: float, upper: float):
        if lower < 0 or lower > upper:
            raise ValueError("Unvalid lower value")
        if upper < 0 or upper > 100:
            raise ValueError("Unvalid upper value")
        self._lower = lower
        self._upper = upper

    def can_open(self) -> bool:
        logger.info("Condition not satisfied!")
