# Fly.io deployment
fly launch --no-deploy
fly secrets set SAMPLEFORGE_API_KEYS='["your-key"]' SAMPLEFORGE_DATABASE_URL=... SAMPLEFORGE_REDIS_URL=...
fly deploy
# run migrations: fly ssh console -C "alembic upgrade head"
