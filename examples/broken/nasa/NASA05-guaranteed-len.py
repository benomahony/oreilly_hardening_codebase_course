# Deliberately broken: lint this file; do not execute it.
def reserve_with_length_padding(quantities):
    count = len(quantities)
    assert count >= 0, "count must not be negative"
    return count
