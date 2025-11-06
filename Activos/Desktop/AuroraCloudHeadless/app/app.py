import os, time, asyncio, httpx
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel

TOKEN = os.getenv("AURORA_CLOUD_TOKEN","changeme")
BIOSPHERE_URL = os.getenv("BIOSPHERE_URL","")
ANO_URL = os.getenv("ANO_URL","")
APP = FastAPI(title="Aurora Headless Runner", version="1.0")

class Ingest(BaseModel):
    source:str
    payload:dict

def _check(token: str|None):
    if not TOKEN: return
    if token!=TOKEN: raise HTTPException(status_code=401, detail="unauthorized")

@APP.get("/health")
def health():
    return {"ok": True, "service": "AURORA_CLOUD_HEADLESS", "version": "1.0"}

@APP.get("/secure/health")
def secure_health(x_aurora_key: str|None = Header(default=None)):
    _check(x_aurora_key); return {"ok": True, "secure": True}

@APP.post("/ingest")
async def ingest(data: Ingest, x_aurora_key: str|None = Header(default=None)):
    _check(x_aurora_key)
    return {"ok": True, "received": data.model_dump()}

@APP.post("/dispatch")
async def dispatch(req: Request, x_aurora_key: str|None = Header(default=None)):
    _check(x_aurora_key)
    body = await req.json()
    async with httpx.AsyncClient(timeout=10) as cx:
        out = {}
        if BIOSPHERE_URL:
            try:
                r = await cx.get(f"{BIOSPHERE_URL}/health"); out["biosphere"]=r.json()
            except Exception as e: out["biosphere"]= {"error": str(e)}
        if ANO_URL:
            try:
                r = await cx.get(f"{ANO_URL}/health"); out["ano"]=r.json()
            except Exception as e: out["ano"]= {"error": str(e)}
    out["echo"]=body
    return {"ok": True, "dispatch": out}

# Background loop (synthetic ops)
async def worker():
    while True:
        await asyncio.sleep(30)

@APP.on_event("startup")
async def startup():
    asyncio.create_task(worker())
