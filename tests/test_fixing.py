from src.parsing import build_price_items
from src.validation import detect_inconsistencies
from src.fixing import fix_products_inplace
from src.fixing import validate_or_fix_avg_prices, DEFAULT_AVG_PRICES

AVG_PRICES = {
    "mtpl": 400.0,
    "limited_casco": 800.0,
    "casco": 1200.0,
}


PRICES_CASE_1_VALID = {
    "mtpl": 400,
    "limited_casco_compact_100": 820,
    "limited_casco_compact_200": 760,
    "limited_casco_compact_500": 650,
    "limited_casco_basic_100": 900,
    "limited_casco_basic_200": 780,
    "limited_casco_basic_500": 600,
    "limited_casco_comfort_100": 963,
    "limited_casco_comfort_200": 870,
    "limited_casco_comfort_500": 720,
    "limited_casco_premium_100": 1030,
    "limited_casco_premium_200": 980,
    "limited_casco_premium_500": 800,
    "casco_compact_100": 1230,
    "casco_compact_200": 1140,
    "casco_compact_500": 975,
    "casco_basic_100": 1350,
    "casco_basic_200": 1170,
    "casco_basic_500": 650,
    "casco_comfort_100": 1444,
    "casco_comfort_200": 1305,
    "casco_comfort_500": 1043,
    "casco_premium_100": 1546,
    "casco_premium_200": 1470,
    "casco_premium_500": 1116,
}



PRICES_CASE_2_NEEDS_FIX = {
    "mtpl": 400,
    "limited_casco_compact_100": 700,
    "limited_casco_compact_200": 720,  # deductible FAIL
    "limited_casco_compact_500": 740,  # deductible FAIL
    "limited_casco_basic_100": 920,    # variant FAIL (basic > comfort/premium)
    "limited_casco_basic_200": 780,
    "limited_casco_basic_500": 600,
    "limited_casco_comfort_100": 850,
    "limited_casco_comfort_200": 870,  # deductible FAIL (200 > 100)
    "limited_casco_comfort_500": 720,
    "limited_casco_premium_100": 880,
    "limited_casco_premium_200": 980,  # deductible FAIL (200 > 100)
    "limited_casco_premium_500": 800,
    "casco_compact_100": 650,          # product FAIL (casco < limited for same variant+deductible)
    "casco_compact_200": 700,          # product FAIL vs limited_casco_compact_200=720
    "casco_compact_500": 620,          # product FAIL vs limited_casco_compact_500=740
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


def test_avg_prices_ok_when_sorted():
    avg = {"mtpl": 200.0, "limited_casco": 500.0, "casco": 700.0}
    out = validate_or_fix_avg_prices(avg, fix_by_sorting=True)
    assert out == avg

def test_avg_prices_wrong_order_fix_false_returns_default():
    avg = {"mtpl": 700.0, "limited_casco": 800.0, "casco": 400.0}
    out = validate_or_fix_avg_prices(avg, fix_by_sorting=False)
    assert out == DEFAULT_AVG_PRICES

def test_avg_prices_wrong_order_fix_true_sorts_and_assigns_by_rank():
    avg = {"mtpl": 700.0, "limited_casco": 800.0, "casco": 400.0}
    out = validate_or_fix_avg_prices(avg, fix_by_sorting=True)
    assert out == {"mtpl": 400.0, "limited_casco": 700.0, "casco": 800.0}

def test_avg_prices_none_returns_default():
    out = validate_or_fix_avg_prices()
    assert out == DEFAULT_AVG_PRICES

def test_fix_keeps_valid_case_valid():
    prices = dict(PRICES_CASE_1_VALID)
    items = build_price_items(prices)

    before = detect_inconsistencies(items, prices)
    assert before.strip() == ""

    fix_products_inplace(items, prices, avg_prices=DEFAULT_AVG_PRICES, max_iters=20)

    after = detect_inconsistencies(items, prices)
    assert after.strip() == ""


def test_fix_removes_inconsistencies():
    prices = dict(PRICES_CASE_2_NEEDS_FIX)
    items = build_price_items(prices)
    avg = {"mtpl": 700.0, "limited_casco": 800.0, "casco": 400.0}
    before = detect_inconsistencies(items, prices)
    assert before.strip() != ""

    fix_products_inplace(items, prices, avg_prices=avg, max_iters=50)

    after = detect_inconsistencies(items, prices)
    assert after.strip() == ""
