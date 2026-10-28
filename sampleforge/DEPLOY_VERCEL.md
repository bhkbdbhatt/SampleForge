# Deploy SampleForge API to Vercel (Free Tier) - Step by Step

This repo is restructured to run the API serverlessly. The ML worker must run separately (Render/Fly.io/Railway/Modal/OnRender free tier etc). 

## Prerequisites
- Vercel account (free)
- Git repo pushed to GitHub/GitLab/Bitbucket
- Separate worker endpoint (see Worker section)
- Managed Postgres (e.g. Neon/Supabase free) and Redis (e.g. Upstash Redis free) accessible from both API and worker

## 1) Prepare the repo
- Ensure `.vercelignore` exists (excludes workers, generation, torch etc)
- Ensure `vercel.json` exists with `@vercel/python` pointing to `api/index.py`
- Ensure `api/index.py` does `from app.main import app`
- Ensure `api/requirements.txt` has minimal deps only

## 2) Configure environment variables (Vercel)
In Vercel Project Settings → Environment Variables add:
```
SAMPLEFORGE_API_KEYS=["your-api-key"]
SAMPLEFORGE_DATABASE_URL=postgresql+asyncpg://...
SAMPLEFORGE_STORAGE_BACKEND=local # or s3
SAMPLEFORGE_QUEUE_BACKEND=http
SAMPLEFORGE_WORKER_ENQUEUE_URL=https://your-worker.example.com
SAMPLEFORGE_WORKER_ENQUEUE_TOKEN=super-secret-token
SAMPLEFORGE_RATE_LIMIT_ENABLED=true
SAMPLEFORGE_GENERATE_RATE_LIMIT=100/minute
SAMPLEFORGE_BATCH_RATE_LIMIT=10/minute
```

Note: Vercel serverless has no persistent disk. If using `local` storage backend, files won't persist across invocations/regions - use S3/Cloudflare R2 for production on Vercel.

## 3) Deploy API on Vercel
Option 1: Import via Vercel Dashboard (Git integration)
1. New Project → Import repo
2. Framework Preset: Other
3. Build Command: (leave empty)
4. Output Directory: (leave empty)
5. Install Command: `pip install -r api/requirements.txt` (or let Vercel use it)
6. Root Directory: `./`
7. Deploy

Option 2: CLI
```bash
npm i -g vercel
vercel login
vercel --prod
```

## 4) Deploy worker separately (required)
The worker needs torch/librosa/scipy/soundfile. Deploy as container/service.
Endpoints needed: worker must expose `POST /enqueue/{job_id}` secured by `SAMPLEFORGE_WORKER_ENQUEUE_TOKEN` that enqueues to its own arq/Redis queue.

Example worker env:
```
SAMPLEFORGE_DATABASE_URL=postgresql+asyncpg://...
SAMPLEFORGE_REDIS_URL=redis://...
S SAMPLEFORGE_STORAGE_BACKER s3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
SAMPLEFORGE_DEVICE=cpu
SAMPLEFORGE_QUEUE_BACKEND=arq
```

Free options:
- Render.com (free web service + background worker, some limits)
- Railway.app (free credits)
- Fly.io (free tier)
- Modal.com (free tier)
- Ploomber Cloud/others

## 5) Run migrations
Before first deploy, run alembic migrations against the managed Postgres DB from a local machine or CI:
```bash
export SAMPLEFORGE_DATABASE_URL=postgresql+asyncpg://...
alembic upgrade head
```

## 6) Verify
- GET https://your-api.vercel.app/v1/health (should return 200)
- POST /v1/generate with API key should return 202 and enqueue via worker
- Worker processes jobs and writes to storage; API serves status via DB

## Troubleshooting
- Bundle size >500MB: ensure `.vercelignore` excludes `app/workers`, `app/generation`, `torch`, etc. Use `requirements-api.txt` only.
- Function timeout: Vercel free has short timeouts; API only enqueues (fast), worker does heavy work.
- No disk: use S3/R2.
- Cold starts: API is light now.
- Import errors: lazy imports are used; ensure only API paths are bundled.
