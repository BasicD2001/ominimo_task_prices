from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PriceElement:
    key: str
    product: str
    variant: Optional[str] = None
    deductible: Optional[int] = None