import os
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True, "service": "aurora-headless"}

@app.get("/secure/health")
def secure_health(x_aurora_key: str = Header(None)):
    token = os.getenv("AURORA_CLOUD_TOKEN", "")
    if not token or x_aurora_key != token:
        raise HTTPException(status_code=401, detail="unauthorized")
    return {"ok": True, "secure": True}
