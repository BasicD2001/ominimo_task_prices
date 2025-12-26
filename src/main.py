from typing import Dict

from src.parsing import build_price_elements
from src.validation import detect_inconsistencies
from src.fixing import fix_products_inplace
from .utils import AVG_PRICES, PRICES_CASE_1, PRICES_CASE_2, PRICES_CASE_3


def print_prices(prices: Dict[str, int]) -> None:
    for k in prices.keys():
        print(f"{k}: {prices[k]}")


def run_case(case_name: str, prices: Dict[str, int]) -> None:
    prices_local = dict(prices)
    items = build_price_elements(prices_local)

    

    print("\n--- PRICES (BEFORE) ---")
    print_prices(prices_local)

    print("\n--- INCONSISTENCIES (BEFORE) ---")
    before_report = detect_inconsistencies(items, prices_local)
    print(before_report if before_report.strip() else "(no inconsistencies found)")

    fix_products_inplace(items, prices_local, avg_prices=AVG_PRICES, max_iters=10)

    print("\n--- INCONSISTENCIES (AFTER) ---")
    after_report = detect_inconsistencies(items, prices_local)
    print(after_report if after_report.strip() else "(no inconsistencies found)")

    print("\n--- PRICES (AFTER) ---")
    print_prices(prices_local)


def run_example() -> None:
    #run_case("CASE 1", PRICES_CASE_1)
    #run_case("CASE 2", PRICES_CASE_2)
    run_case("CASE 3", PRICES_CASE_3)


if __name__ == "__main__":
    run_example()
