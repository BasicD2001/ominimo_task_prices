
from typing import Callable, Dict, List, Optional

from .models import PriceElement


def group_items(items: List[PriceElement], predicate: Callable[[PriceElement], bool]) -> List[PriceElement]:
    return [it for it in items if predicate(it)]


def max_price_in_group(
    items: List[PriceElement],
    prices: Dict[str, int],
    predicate: Callable[[PriceElement], bool],
) -> Optional[int]:
    mx: Optional[int] = None
    for it in items:
        if predicate(it):
            p = prices[it.key]
            mx = p if mx is None else max(mx, p)
    return mx


def min_price_in_group(
    items: List[PriceElement],
    prices: Dict[str, int],
    predicate: Callable[[PriceElement], bool],
) -> Optional[int]:
    mn: Optional[int] = None
    for it in items:
        if predicate(it):
            p = prices[it.key]
            mn = p if mn is None else min(mn, p)
    return mn
