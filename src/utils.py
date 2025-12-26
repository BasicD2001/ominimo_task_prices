
from typing import Callable, Dict, List, Optional
from dataclasses import dataclass


# parsing class
@dataclass(frozen=True)
class PriceElement:
    key: str
    product: str
    variant: Optional[str] = None
    deductible: Optional[int] = None


#priority ranks and safe getters
product_rank = {
    "mtpl": 1,
    "limited_casco": 2,
    "casco": 3,
}

variants_rank = {
    "compact": 1,
    "basic": 1,
    "comfort": 2,
    "premium": 3,
}

deductibles_rank = {
    100: 1,
    200: 2,
    500: 3,
}

core_product = {"mtpl"}


def is_core_product(product: str) -> bool:
    return product in core_product


def get_product_rank(product: str) -> int:
    try:
        return product_rank[product]
    except KeyError as e:
        raise KeyError(f"Unknown product key: {product!r}") from e


def get_variant_rank(variant: str) -> int:
    try:
        return variants_rank[variant]
    except KeyError as e:
        raise KeyError(f"Unknown variant key: {variant!r}") from e


def get_deductible_rank(deductible: int) -> int:
    try:
        return deductibles_rank[deductible]
    except KeyError as e:
        raise KeyError(f"Unknown deductible key: {deductible!r}") from e



#helper functions
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



#default avg_prices
AVG_PRICES = {"mtpl": 400.0, "limited_casco": 800.0, "casco": 1200.0}



#price_cases
PRICES_CASE_1 = {
    "mtpl": 400,
    "limited_casco_compact_100": 820,
    "limited_casco_compact_200": 760,
    "limited_casco_compact_500": 650,
    "limited_casco_basic_100": 900,
    "limited_casco_basic_200": 780,
    "limited_casco_basic_500": 600,
    "limited_casco_comfort_100": 850,
    "limited_casco_comfort_200": 870,
    "limited_casco_comfort_500": 720,
    "limited_casco_premium_100": 880,
    "limited_casco_premium_200": 980,
    "limited_casco_premium_500": 800,
    "casco_compact_100": 750,
    "casco_compact_200": 700,
    "casco_compact_500": 620,
    "casco_basic_100": 830,
    "casco_basic_200": 760,
    "casco_basic_500": 650,
    "casco_comfort_100": 900,
    "casco_comfort_200": 820,
    "casco_comfort_500": 720,
    "casco_premium_100": 1050,
    "casco_premium_200": 950,
    "casco_premium_500": 1040,
}


PRICES_CASE_2 = {
    "mtpl": 400,
    "limited_casco_compact_100": 900,
    "limited_casco_compact_200": 760,
    "limited_casco_compact_500": 650,
    "limited_casco_basic_100": 950,
    "limited_casco_basic_200": 780,
    "limited_casco_basic_500": 600,
    "limited_casco_comfort_100": 850,
    "limited_casco_comfort_200": 870,
    "limited_casco_comfort_500": 720,
    "limited_casco_premium_100": 880,
    "limited_casco_premium_200": 980,
    "limited_casco_premium_500": 800,
    "casco_compact_100": 850,
    "casco_compact_200": 700,
    "casco_compact_500": 620,
    "casco_basic_100": 880,
    "casco_basic_200": 760,
    "casco_basic_500": 650,
    "casco_comfort_100": 900,
    "casco_comfort_200": 820,
    "casco_comfort_500": 720,
    "casco_premium_100": 1050,
    "casco_premium_200": 950,
    "casco_premium_500": 1040,
}


PRICES_CASE_3 = {
"mtpl": 400,
"limited_casco_compact_100": 820,
"limited_casco_compact_200": 760,
"limited_casco_compact_500": 650,
"limited_casco_basic_100": 900,
"limited_casco_basic_200": 780,
"limited_casco_basic_500": 600,
"limited_casco_comfort_100": 950,
"limited_casco_comfort_200": 870,
"limited_casco_comfort_500": 720,
"limited_casco_premium_100": 1100,
"limited_casco_premium_200": 980,
"limited_casco_premium_500": 800,
"casco_compact_100": 750,
"casco_compact_200": 700,
"casco_compact_500": 620,
"casco_basic_100": 830,
"casco_basic_200": 760,
"casco_basic_500": 650,
"casco_comfort_100": 900,
"casco_comfort_200": 820,
"casco_comfort_500": 720,
"casco_premium_100": 1050,
"casco_premium_200": 950,
"casco_premium_500": 780
}
