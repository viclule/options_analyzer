from typing import Text, Optional

from pydantic import BaseModel

from options_freedom.symbol.symbol import Symbol
from options_freedom.conditions.base import Condition
from options_freedom.pattern.base import Pattern


class Strategy(BaseModel):
    under: Symbol
    open_condition: Condition
    close_condition: Condition
    pattern: Pattern
