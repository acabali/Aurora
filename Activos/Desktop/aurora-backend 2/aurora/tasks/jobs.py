from aurora.tasks.app import celery_app
from aurora.pipelines import ingest
from aurora.knowledge import store
@celery_app.task
def init_knowledge():
    store.init()
    return "ok"
@celery_app.task
def ingest_local():
    return ingest.ingest_local_folder()
@celery_app.task
def ingest_rss_task(url: str):
    return ingest.ingest_rss(url)
