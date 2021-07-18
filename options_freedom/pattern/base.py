from pydantic import BaseModel


class Pattern(BaseModel):
    commissions: float
