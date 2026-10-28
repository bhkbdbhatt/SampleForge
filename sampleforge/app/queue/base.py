"""Queue interface base (API-safe)."""
from __future__ import annotations

from typing import Protocol


class QueueUnavailableError(Exception):
    """Raised when the queue backend is unreachable."""


class QueueBackend(Protocol):
    async def enqueue(self, job_id: str) -> str | None: ...


async def enqueue_job(job_id: str) -> str | None:
    """Enqueue via configured backend. Falls back to arq for backward compat."""
    from app.core.config import settings

    backend = getattr(settings, "queue_backend", "arq")
    if backend == "http":
        from app.queue.http import enqueue_job as _enqueue

        return await _enqueue(job_id)
    # Default to existing arq backend (used by worker)
    try:
        from app.workers.queue import enqueue_job as _enqueue

        return await _enqueue(job_id)
    except Exception as exc:
        from app.queue.base import QueueUnavailableError

        raise QueueUnavailableError(str(exc)) from exc
