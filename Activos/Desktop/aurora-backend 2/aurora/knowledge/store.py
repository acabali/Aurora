from dataclasses import dataclass
from typing import List, Union, Any
from sqlalchemy import text
from aurora.core.db import engine, SessionLocal
from aurora.core.embeddings import embed_texts

@dataclass
class Doc:
    id: int | None
    source: str
    title: str
    content: str
    tags: list[str]

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS documents(
  id SERIAL PRIMARY KEY,
  source TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  tags TEXT[] DEFAULT '{}',
  embedding vector(384)
);
CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops);
"""

def _to_vector_literal(vec: Any) -> str:
    # Devuelve el string "[1.0,2.0,...]" que CAST(... AS vector) acepta.
    out = []
    for x in vec:
        try:
            out.append(float(x))
        except Exception:
            s = str(x).replace('np.float64(','').replace(')','')
            out.append(float(s))
    return "[" + ",".join(str(v) for v in out) + "]"

def _coerce_doc(x: Union[Doc, dict, str]) -> Doc:
    if isinstance(x, Doc):
        return x
    if isinstance(x, dict):
        return Doc(
            id=None,
            source=str(x.get("source","")),
            title=str(x.get("title","")),
            content=str(x.get("content","")),
            tags=list(x.get("tags",[]) or []),
        )
    # último recurso: si viene string suelto
    return Doc(id=None, source="", title="", content=str(x), tags=[])

def init():
    # asegura tablas/índices
    with engine.begin() as conn:
        conn.execute(text(SCHEMA_SQL))

def add_documents(docs: List[Union[Doc, dict, str]]):
    if not docs:
        return
    norm = [_coerce_doc(d) for d in docs]
    embs = embed_texts([d.content for d in norm])
    with engine.begin() as conn:
        for d, emb in zip(norm, embs):
            vec = _to_vector_literal(emb)
            conn.execute(
                text("INSERT INTO documents(source,title,content,tags,embedding) "
                     "VALUES (:s,:t,:c,:g,CAST(:e AS vector))"),
                {"s": d.source, "t": d.title, "c": d.content, "g": d.tags, "e": vec}
            )

def search(query: str, limit: int = 5):
    # fallback simple: últimos N (evita fallar aunque no haya embedding)
    with SessionLocal() as s:
        rows = s.execute(
            text("""
                SELECT id, source, title, content, tags
                FROM documents
                ORDER BY id DESC
                LIMIT :lim
            """),
            {"lim": limit}
        ).fetchall()
        return [dict(r._mapping) for r in rows]
