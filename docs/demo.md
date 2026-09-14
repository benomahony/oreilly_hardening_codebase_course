# Presenter walkthrough

The [README](../README.md) is the command list. Every teaching file runs with
`uv run FILE`, contains its own tests, and explains its live edit at the top.

1. Show the stock counter: ten minus three should leave seven.
2. Run `uv run examples/assertions/test_off_by_one.py`. With `+ 1` in the
   calculation, Hypothesis shrinks the failure to one requested unit. Remove the
   `+ 1`, rerun the same file, and show green.
3. Pick a static-check lesson from the README. Run its file, read the diagnostic,
   fix the code in that file, and rerun it. NASA and Test Desiderata offer extra
   small examples for individual rules.
4. Run `uv run examples/mutation/test_weak_suite.py`. The positive-stock test
   passes while the zero-stock case fails. Change `> 0` to `>= 0` and rerun.
5. Finish with `make check` to show the complete application's checks in CI.

Edit the code or test named in the instruction; keep the checker and launcher
intact. Undo your changes after each lesson to reset it. A fixed example should stay green when run again.

The [exercise reference](exercises.md) explains the fixes in more detail. Mutation
testing with the real tool is covered in [the mutation notes](mutation.md).
Before going offline, run `uv sync --locked` and a domain-language example once
to populate the dependency and parser caches.
