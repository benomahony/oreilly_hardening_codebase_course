# Deliberately broken: lint this file; do not execute it.
def reserve_with_compound_contract(stock, units):
    assert stock >= 0 and units > 0, "stock and units must be valid"
    return stock - units
