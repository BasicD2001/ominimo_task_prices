# src/ominimo_task/validation.py

from typing import Dict, List

from .models import PriceElement
from .ranks import core_product, get_deductible_rank, get_product_rank, get_variant_rank


def detect_inconsistencies(items: List[PriceElement], prices: Dict[str, int]) -> str:
    report: List[str] = []
    n = len(items)

    for i in range(n):
        for j in range(i + 1, n):
            a = items[i]
            b = items[j]

            price_a = prices[a.key]
            price_b = prices[b.key]

            pa = get_product_rank(a.product)
            pb = get_product_rank(b.product)

            # Core vs non-core product ordering constraint 
            if pa != pb:
    
                lower, higher, lower_price, higher_price= (a, b, price_a, price_b) if pa < pb  else (b,a, price_b, price_a)

                if lower.product in core_product and lower_price >= higher_price:
                    report.append(
                        f"PRODUCT ORDER: '{lower.key}' ({lower_price}) should be cheaper than '{higher.key}' ({higher_price})."
                    )

            # Product ordering when same variant + deductible (both non-core)
            if (
                a.product != b.product
                and a.variant == b.variant
                and a.deductible == b.deductible
            ):
                pa2 = get_product_rank(a.product)
                pb2 = get_product_rank(b.product)

                lower_p, higher_p, lower_price, higher_price= (a, b, price_a, price_b) if pa2 < pb2  else (b,a, price_b, price_a)

                if lower_price >= higher_price:
                    report.append(
                        f"PRODUCT ORDER (same variant+deductible): '{lower_p.key}' ({lower_price}) should be cheaper than '{higher_p.key}' ({higher_price})."
                    )

            # Variant ordering within product for same deductible (both non-core)
            if (
                a.product == b.product
                and a.deductible == b.deductible
            ):
                va = get_variant_rank(a.variant)
                vb = get_variant_rank(b.variant)

                if va != vb:

                    lower_v, higher_v, lower_price, higher_price= (a, b, price_a, price_b) if va < vb  else (b,a, price_b, price_a)

                    if lower_price >= higher_price:
                        report.append(
                            f"VARIANT ORDER: '{lower_v.key}' ({lower_price}) should be cheaper than '{higher_v.key}' ({higher_price})."
                        )

            # Deductible ordering within product for same variant (both non-core)
            if (
                a.product == b.product
                and a.variant == b.variant
            ):
                da = get_deductible_rank(a.deductible)
                db = get_deductible_rank(b.deductible)

                if da != db:

                    lower_d, higher_d, lower_price, higher_price= (a, b, price_a, price_b) if da < db  else (b,a, price_b, price_a)

                    if higher_price >= lower_price:
                        report.append(
                            f"DEDUCTIBLE ORDER: '{higher_d.key}' ({higher_price}) should be cheaper than '{lower_d.key}' ({lower_price})."
                        )

    return "\n".join(report)
