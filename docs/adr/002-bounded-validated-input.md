# ADR 002: Bound input before it reaches the domain

Status: accepted.

Context: callers control bytes, and Python annotations do not validate them.
Decision: accept 1–32 quantities, each 1–9999, with a 159-byte ceiling. Reject
bad input with explicit exceptions; use assertions for internal contracts.
Consequence: validation still works with `python -O`; the defensive domain
assertions require normal, unoptimized Python. CI checks both behaviors.

```python
from reservations.infrastructure.wire import parse_reservations

assert parse_reservations(b",".join([b"9999"] * 32)) == (9999,) * 32
for payload in (b"0", b"-1", b"1\n", b"1" * 160):
    try:
        parse_reservations(payload)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid external input must be rejected")
```
