from typing import Optional

from options_freedom.models.constants import comission_per_contract
from options_freedom.option.base import Option
from options_freedom.pattern.base import Pattern


class BullPutSpread(Pattern):
    commissions: Optional[float] = 2 * comission_per_contract
    wrote_put: Option
    bought_put: Option
