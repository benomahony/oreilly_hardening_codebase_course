# Deliberately broken: lint this file; do not execute it.
def reserve_with_padding():
    stock = 10
    assert stock > 0, "stock is positive"
    return stock
