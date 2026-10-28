from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/v1/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
