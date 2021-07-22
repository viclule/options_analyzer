from typing import List

from pydantic import BaseModel

from options_freedom.option.base import Option


class Pattern(BaseModel):
    commissions: float

    written: List[Option]
    bougth: List[Option]

    def bid(self) -> float:
        pass

    def ask(self) -> float:
        pass
