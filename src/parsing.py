
from typing import Dict, List

from .models import PriceElement
from .ranks import core_product


def parse_price_key(input_key: str) -> PriceElement:
    parts = input_key.split("_")

    if parts[:2] == ["limited", "casco"] and len(parts) == 4:
        product = "limited_casco"
        variant = parts[2]
        deductible = int(parts[3])
        return PriceElement(key=input_key, product=product, variant=variant, deductible=deductible)

    if len(parts) == 3:
        product = parts[0]
        variant = parts[1]
        deductible = int(parts[2])
        return PriceElement(key=input_key, product=product, variant=variant, deductible=deductible)

    raise ValueError(f"Unrecognized key format: {input_key!r}")


def build_price_elements(prices: Dict[str, int]) -> List[PriceElement]:
    items: List[PriceElement] = []
    for input_key in prices.keys():
        if input_key in core_product:
            items.append(PriceElement(key=input_key, product=input_key))
        else:
            items.append(parse_price_key(input_key))
    return items
