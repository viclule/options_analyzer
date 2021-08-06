from typing import Optional

from options_freedom.models.constants import comission_per_contract
from options_freedom.pattern.base import Pattern


class IronCondor(Pattern):
    # divided by 100 to adjust to option prices based on 100 shares
    commissions: Optional[float] = 8 * comission_per_contract / 100.0

    @property
    def max_loss(self):
        return self.commissions + self.short[0].strike - self.long[0].strike
