# Vercel deployment notes
- Set env vars: SAMPLEFORGE_DATABASE_URL, SAMPLEFORGE_API_KEYS, SAMPLEFORGE_QUEUE_BACKEND=http, SAMPLEFORGE_WORKER_ENQUEUE_URL, SAMPLEFORGE_WORKER_ENQUEUE_TOKEN
- Do NOT include torch/librosa in API bundle
- Deploy worker separately (Render/Fly.io/Railway/Modal) with full deps
- Use managed Postgres/Redis accessible from both
