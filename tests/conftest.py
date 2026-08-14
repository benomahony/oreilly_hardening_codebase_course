"""Technique 6: Hypothesis profiles. Select with `HYPOTHESIS_PROFILE=ci uv
run pytest`. `dev` (default) is fast enough for every save; `ci` spends far
more examples finding what `dev` would miss; `debug` adds verbose shrinking
output; `fast` is for a tight inner loop."""

from __future__ import annotations

import os

from hypothesis import HealthCheck, Verbosity, settings

settings.register_profile("dev", max_examples=100, deadline=None)
settings.register_profile(
    "ci", max_examples=1000, deadline=None, suppress_health_check=[HealthCheck.too_slow]
)
settings.register_profile("debug", max_examples=10, deadline=None, verbosity=Verbosity.verbose)
settings.register_profile("fast", max_examples=10, deadline=None)

settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "dev"))
