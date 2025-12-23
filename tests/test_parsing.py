import pytest

from src.parsing import parse_price_key, build_price_items


def test_parse_mtpl_raises():
    with pytest.raises(ValueError):
        parse_price_key("mtpl")


def test_parse_regular_key():
    item = parse_price_key("casco_basic_200")
    assert item.product == "casco"
    assert item.variant == "basic"
    assert item.deductible == 200


def test_parse_limited_casco_key():
    item = parse_price_key("limited_casco_premium_500")
    assert item.product == "limited_casco"
    assert item.variant == "premium"
    assert item.deductible == 500


def test_build_price_items_includes_core_product():
    prices = {"mtpl": 400, "casco_basic_200": 760}
    items = build_price_items(prices)

    mtpl_item = next(x for x in items if x.key == "mtpl")
    assert mtpl_item.product == "mtpl"
    assert mtpl_item.variant is None
    assert mtpl_item.deductible is None


def test_build_price_items_parses_non_core_product():
    prices = {"casco_basic_200": 760}

    items = build_price_items(prices)

    assert len(items) == 1
    item = items[0]

    assert item.key == "casco_basic_200"
    assert item.product == "casco"
    assert item.variant == "basic"
    assert item.deductible == 200
    assert item.key == "casco_basic_200"
