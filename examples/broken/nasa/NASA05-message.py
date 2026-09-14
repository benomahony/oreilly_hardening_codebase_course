# Deliberately broken: lint this file; do not execute it.
def reserve_without_messages(stock, units):
    assert stock >= 0
    assert units > 0
    return stock - units
