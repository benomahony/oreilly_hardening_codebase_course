from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BotMetrics:
    commands_processed: int = 0
    commands_failed: int = 0
    tasks_created: int = 0
    tasks_completed: int = 0

    def record_command(self, *, failed: bool) -> None:
        assert isinstance(failed, bool), "failed must be a bool"
        assert self.commands_processed >= 0, "commands_processed went negative"
        self.commands_processed += 1
        if failed:
            self.commands_failed += 1

    def record_task_created(self) -> None:
        self.tasks_created += 1

    def record_task_completed(self) -> None:
        self.tasks_completed += 1

    @property
    def failure_rate(self) -> float:
        """Fraction of processed commands that failed, in [0.0, 1.0]. See
        tests/unit/test_metrics.py."""
        if self.commands_processed == 0:
            return 0.0
        rate = self.commands_failed / self.commands_processed
        assert 0.0 <= rate <= 1.0, f"failure_rate out of range: {rate}"
        return rate
