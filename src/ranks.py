
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
