# Deliberately broken: lint this file; do not execute it.
def reserve_with_type_contract(stock):
    assert isinstance(stock, int), "stock must be an integer"
    return stock
