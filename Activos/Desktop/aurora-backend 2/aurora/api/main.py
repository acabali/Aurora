from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from aurora.knowledge import store
from aurora.pipelines import ingest

app = FastAPI()

@app.on_event("startup")
def _startup():
    store.init()

class SearchResponse(BaseModel):
    results: List[dict]

@app.get("/health")
def health():
    return {"status":"ok","env":"dev","objective":"Evolve into SURPA: non-generic, innovative, fast, efficient"}

@app.post("/ingest/rss")
def ingest_rss(url: str = Query(...)):
    # Blindar: no tiramos 500 aunque algo falle.
    try:
        docs = ingest.ingest_rss(url)  # puede devolver list[dict|Doc|str]
        if docs:
            store.add_documents(docs)
        return {"status":"ok","ingested": len(docs) if docs else 0}
    except Exception as e:
        # devolvemos 200 con detalle para que no corte el flujo
        return {"status":"skipped","reason": str(e)}

@app.get("/search", response_model=SearchResponse)
def search(q: str = Query(...), limit: int = 5):
    return {"results": store.search(q, limit=limit)}

@app.get("/agents")
def list_agents():
    return [{"id":"default","name":"Aurora"}]
