from src.parsing import build_price_elements
from src.validation import detect_inconsistencies



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

# CASE 2: PRODUCT ORDER (same variant+deductible) problem:

PRICES_CASE_2_PRODUCT_ORDER_FAIL = {
    "mtpl": 400,
    "limited_casco_compact_100": 900,
    "limited_casco_compact_200": 760,
    "limited_casco_compact_500": 650,
    "limited_casco_basic_100": 950,
    "limited_casco_basic_200": 780,
    "limited_casco_basic_500": 600,
    "limited_casco_comfort_100": 920,
    "limited_casco_comfort_200": 870,
    "limited_casco_comfort_500": 720,
    "limited_casco_premium_100": 980,
    "limited_casco_premium_200": 980,
    "limited_casco_premium_500": 800,
    "casco_compact_100": 850,   # FAIL:should be > limited_casco_compact_100
    "casco_compact_200": 700,
    "casco_compact_500": 620,
    "casco_basic_100": 880,     # FAIL
    "casco_basic_200": 760,
    "casco_basic_500": 650,
    "casco_comfort_100": 890,   # FAIL
    "casco_comfort_200": 820,
    "casco_comfort_500": 720,
    "casco_premium_100": 970,   # FAIL
    "casco_premium_200": 950,
    "casco_premium_500": 1040,
}

# CASE 3: DEDUCTIBLE ORDER problem
PRICES_CASE_3_DEDUCTIBLE_ORDER_FAIL = {
    "mtpl": 400,
    "limited_casco_compact_100": 700,
    "limited_casco_compact_200": 720,  # FAIL
    "limited_casco_compact_500": 740,  # FAIL
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



# CASE 4: TASK INPUT

PRICES_CASE_4_EXAMPLE_FROM_TASK = {
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



PRICES_CASE_5_VARIANT_ORDER_FAIL = {
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
    "casco_comfort_500": 1117, # 1117 > 1116 (casco_premium_500)
    "casco_premium_100": 1546,
    "casco_premium_200": 1470,
    "casco_premium_500": 1116,
}


def test_case_1_has_no_inconsistencies():
    items = build_price_elements(PRICES_CASE_1_VALID)
    report = detect_inconsistencies(items, PRICES_CASE_1_VALID)
    assert report.strip() == ""


def test_case_2_detects_product_order_same_variant_deductible():
    items = build_price_elements(PRICES_CASE_2_PRODUCT_ORDER_FAIL)
    report = detect_inconsistencies(items, PRICES_CASE_2_PRODUCT_ORDER_FAIL)
    assert "PRODUCT ORDER (same variant+deductible)" in report


def test_case_3_detects_deductible_order():
    items = build_price_elements(PRICES_CASE_3_DEDUCTIBLE_ORDER_FAIL)
    report = detect_inconsistencies(items, PRICES_CASE_3_DEDUCTIBLE_ORDER_FAIL)
    assert "DEDUCTIBLE ORDER" in report



def test_case_4_detects_product_order_example_from_task():
    items = build_price_elements(PRICES_CASE_4_EXAMPLE_FROM_TASK)
    report = detect_inconsistencies(items, PRICES_CASE_4_EXAMPLE_FROM_TASK)
    assert "PRODUCT ORDER (same variant+deductible)" in report



def test_case_5_detects_variant_order():
    items = build_price_elements(PRICES_CASE_5_VARIANT_ORDER_FAIL)
    report = detect_inconsistencies(items, PRICES_CASE_5_VARIANT_ORDER_FAIL)
    assert "VARIANT ORDER" in report