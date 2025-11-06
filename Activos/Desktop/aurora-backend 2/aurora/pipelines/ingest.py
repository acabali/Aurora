from pathlib import Path
import feedparser, httpx
from bs4 import BeautifulSoup
from aurora.knowledge.store import add_documents, Doc
from aurora.core.config import get_settings
settings = get_settings()
def ingest_local_folder(root: str | None = None):
    root = root or settings.ingest_local_root
    docs = []
    for p in Path(root).rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".txt"}:
            text = p.read_text(encoding="utf-8", errors="ignore")
            docs.append(Doc(id=None, source=f"file:{p}", title=p.name, content=text, tags=["local"]))
    if docs: add_documents(docs)
    return {"added": len(docs)}
def ingest_rss(url: str):
    feed = feedparser.parse(url)
    docs = []
    for e in feed.entries[:20]:
        content = getattr(e, "summary", "") or getattr(e, "description", "") or ""
        title = e.get("title", "RSS item")
        docs.append(Doc(id=None, source=url, title=title, content=content, tags=["rss"]))
    if docs: add_documents(docs)
    return {"added": len(docs)}
async def ingest_url(url: str):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text("\n")
        add_documents([Doc(id=None, source=url, title=soup.title.string if soup.title else url, content=text, tags=["web"])])
    return {"added": 1}
