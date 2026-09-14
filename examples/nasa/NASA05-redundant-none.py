# Deliberately broken: lint this file; do not execute it.
def reserve_with_redundant_contract(stock):
    assert stock is not None, "stock must exist"
    assert isinstance(stock, int), "stock must be an integer"
    return stock
