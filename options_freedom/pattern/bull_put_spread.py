from typing import Optional

from options_freedom.models.constants import comission_per_contract
from options_freedom.pattern.base import Pattern


class BullPutSpread(Pattern):
    commissions: Optional[float] = 2 * comission_per_contract

    @property
    def max_loss(self):
        return self.commissions + self.short[0].strike - self.long[0].strike
