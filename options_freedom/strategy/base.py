from typing import Text, Optional

from pydantic import BaseModel

from options_freedom.symbol.base import Symbol
from options_freedom.conditions.base import OpenCondition, CloseCondition
from options_freedom.pattern.base import Pattern


class Strategy(BaseModel):
    under: Symbol
    open_condition: OpenCondition
    close_condition: CloseCondition
    pattern: Pattern
