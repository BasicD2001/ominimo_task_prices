# src/ominimo_task/fixing.py

from typing import Dict, List, Optional

from .models import PriceElement
from .ranks import (
    get_deductible_rank,
    get_product_rank,
    get_variant_rank,
    is_core_product,
    product_rank

)
from .utils import group_items, max_price_in_group, min_price_in_group


DEFAULT_AVG_PRICES: Dict[str, float] = {"mtpl": 400.0, "limited_casco": 800.0, "casco": 1200.0}



def scale_product(items: List[PriceElement], prices: Dict[str, int], product: str, factor: float) -> bool:
    changed = False
    for it in items:
        if it.product == product:
            new_val = int(round(prices[it.key] * factor))
            if new_val != prices[it.key]:
                prices[it.key] = new_val
                changed = True
    return changed


def scale_deductable(group: List[PriceElement], prices: Dict[str, int], base: int) -> bool:
    changed = False
    for it in group:
        r = get_deductible_rank(it.deductible)
        new_price = int(round(base * (0.9 ** (r - 1))))
        if new_price != prices[it.key]:
            prices[it.key] = new_price
            changed = True
    return changed


def scale_variant(group: List[PriceElement], prices: Dict[str, int], base: int) -> bool:
    changed = False
    for it in group:
        r = get_variant_rank(it.variant)
        if( r>1 ):
            new_price = int(round(base * (1.07 ** (r - 1))))
            if new_price != prices[it.key]:
                prices[it.key] = new_price
                changed = True
    return changed



def validate_or_fix_avg_prices(
    avg_prices: Optional[Dict[str, float]] = None,
    default_avg_prices: Dict[str, float] = DEFAULT_AVG_PRICES,
    fix_by_sorting: bool = True,
) -> Dict[str, float]:
    
    # required_products= {mtpl, limited_casco, casco}
    required_products = list(product_rank.keys())

    # if nothing provided, use DEFAULT_AVG_PRICES
    if avg_prices is None:
        return dict(default_avg_prices)

    # must contain all required products
    for p in required_products:
        if p not in avg_prices:
            return dict(default_avg_prices)

    # values must be numeric and > 0
    values: Dict[str, float] = {}
    for p in required_products:
        try:
            v = float(avg_prices[p])
        except (TypeError, ValueError):
            return dict(default_avg_prices)

        if v <= 0:
            return dict(default_avg_prices)

        values[p] = v
    # from now, values is valid prices dictionary

    # sort products by rank (1,2,3...) and check monotonicity
    prods_by_rank = sorted(required_products, key=product_rank.get)
    seq = [values[p] for p in prods_by_rank]

    ok = True
    for i in range(len(seq) - 1):
        if seq[i] > seq[i + 1]:
            ok = False
            break

    if ok:
        return values

    # if fix_by_sorting== True, sort prices and use it as avg_prices, if not use DEFAULT_AVG_PRICES instead
    if fix_by_sorting:
        sorted_vals = sorted(seq)
        fixed: Dict[str, float] = {}
        for i, p in enumerate(prods_by_rank):
            fixed[p] = sorted_vals[i]
        return fixed

    return dict(default_avg_prices)


def fix_products_inplace(
    items: List[PriceElement],
    prices: Dict[str, int],
    avg_prices: Optional[Dict[str, float]] = None,
    max_iters: int = 10,
) -> None:
    
    avg_prices = validate_or_fix_avg_prices(avg_prices)

    for _ in range(max_iters):
        changed = False
        n = len(items)

        for i in range(n):
            for j in range(i + 1, n):
                a = items[i]
                b = items[j]

                pa = get_product_rank(a.product)
                pb = get_product_rank(b.product)

                a_is_core = is_core_product(a.product)
                b_is_core = is_core_product(b.product)

                va = None if a_is_core else get_variant_rank(a.variant)
                vb = None if b_is_core else get_variant_rank(b.variant)
                da = None if a_is_core else get_deductible_rank(a.deductible)
                db = None if b_is_core else get_deductible_rank(b.deductible)

                if pa != pb:
                    lower, higher = (a, b) if pa < pb else (b, a)
                    lower_price = prices[lower.key]
                    higher_price = prices[higher.key]

                    lower_is_core = is_core_product(lower.product)
                    higher_is_core = is_core_product(higher.product)

                    avg_low = avg_prices.get(lower.product)
                    avg_high = avg_prices.get(higher.product)

                    
                    if not avg_low or not avg_high:
                        continue

                    ratio = avg_high / avg_low

                    if lower_price >= higher_price:
                        # same variant+deductible scaling (non-core to non-core)
                        if (
                            (not lower_is_core)
                            and (not higher_is_core)
                            and (lower.variant == higher.variant)
                            and (lower.deductible == higher.deductible)
                        ):
                            old_h = prices[higher.key]
                            new_h = int(round(lower_price * ratio))
                            if old_h != 0:
                                factor = new_h / old_h
                                prices[higher.key] = new_h
                                changed =True

                        # core vs non-core scaling using min of higher product
                        if lower_is_core and (not higher_is_core):
                            old_min = min_price_in_group(items, prices, lambda it: it.product == higher.product)
                            if old_min is not None and old_min != 0:
                                new_min = int(round(lower_price * ratio))
                                factor = new_min / old_min
                                changed |= scale_product(items, prices, higher.product, factor)

                else:
                    # deductible schedule within same product+variant
                    if (not a_is_core) and (not b_is_core) and (va == vb) and (da != db):
                        lower_d, higher_d = (a, b) if da < db else (b, a)
                        lower_price = prices[lower_d.key]
                        higher_price = prices[higher_d.key]

                        if lower_price <= higher_price:
                            group = group_items(
                                items,
                                lambda it: (
                                    it.product == a.product
                                    and (not is_core_product(it.product))
                                    and it.variant == a.variant
                                ),
                            )
                            base = max_price_in_group(group, prices, lambda it: get_deductible_rank(it.deductible) == 1)
                            if base is not None:
                                changed |= scale_deductable(group, prices, base)

                    # variant schedule within same product+deductible
                    if (not a_is_core) and (not b_is_core) and (da == db) and (va != vb):
                        lower_v, higher_v = (a, b) if va < vb else (b, a)
                        lower_price = prices[lower_v.key]
                        higher_price = prices[higher_v.key]

                        if lower_price >= higher_price:
                            group = group_items(
                                items,
                                lambda it: (
                                    it.product == a.product
                                    and (not is_core_product(it.product))
                                    and it.deductible == a.deductible
                                ),
                            )
                            base = max_price_in_group(group, prices, lambda it: get_variant_rank(it.variant) == 1)
                            if base is not None:
                                changed |= scale_variant(group, prices, base)

        if not changed:
            break
