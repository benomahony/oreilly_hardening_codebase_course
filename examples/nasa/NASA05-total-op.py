# Deliberately broken: lint this file; do not execute it.
def reserve_with_string_contract(stock):
    label = str(stock)
    assert label, "stock label must exist"
    return label
