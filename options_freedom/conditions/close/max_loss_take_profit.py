import logging

from options_freedom.conditions.base import CloseCondition

logger = logging.getLogger(__name__)


class MaxLossTakeProfit(CloseCondition):
    def __init__(self, max_loss_percent: float, take_profit_percent: float):
        if max_loss_percent < 0:
            raise ValueError("Unvalid value")
        if take_profit_percent < 0:
            raise ValueError("Unvalid value")
        self._max_loss_percent = max_loss_percent
        self._take_profit_percent = take_profit_percent

    def can_close(self, p_l: float, max_profit: float) -> bool:
        if p_l < 0:
            p_l = abs(p_l)
            if 100.0 * p_l / max_profit >= self._max_loss_percent:
                logger.info("Max loss - condition satisfied!")
                return True
        else:
            if 100.0 * p_l / max_profit >= self._take_profit_percent:
                logger.info("Take profit - condition satisfied!")
                return True
        return False
