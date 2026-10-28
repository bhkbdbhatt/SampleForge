"""Queue interface base (API-safe)."""
from __future__ import annotations

from typing import Protocol


class QueueUnavailableError(Exception):
    """Raised when the queue backend is unreachable."""


class QueueBackend(Protocol):
    async def enqueue(self, job_id: str) -> str | None: ...


async def enqueue_job(job_id: str) -> str | None:
    """Enqueue via configured backend."""
    from app.core.config import settings

    backend = getattr(settings, "queue_backend", "arq")
    if backend == "http":
        from app.queue.http import enqueue_job as _enqueue

        return await _enqueue(job_id)
    # Try arq only if available (worker environment)
    try:
        from app.workers.queue import enqueue_job as _enqueue  # lazy

        return await _enqueue(job_id)
    except Exception as exc:
        raise QueueUnavailableError(str(exc)) from exc
