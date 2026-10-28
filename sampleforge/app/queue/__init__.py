"""Queue interface for API (no heavy deps)."""
from __future__ import annotations

from app.queue.base import enqueue_job, QueueUnavailableError

__all__ = ["enqueue_job", "QueueUnavailableError"]
