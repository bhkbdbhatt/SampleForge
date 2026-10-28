"""HTTP queue backend for serverless API (no arq import)."""
from __future__ import annotations

import httpx

from app.core.config import settings


class QueueUnavailableError(Exception):
    pass


async def enqueue_job(job_id: str) -> str | None:
    url = getattr(settings, "worker_enqueue_url", None)
    if not url:
        raise QueueUnavailableError("worker_enqueue_url not configured")
    token = getattr(settings, "worker_enqueue_token", None)
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{url.rstrip('/')}/enqueue/{job_id}", headers=headers)
            resp.raise_for_status()
        return job_id
    except Exception as exc:
        raise QueueUnavailableError(str(exc)) from exc
