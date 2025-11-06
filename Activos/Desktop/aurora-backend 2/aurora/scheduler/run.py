from apscheduler.schedulers.blocking import BlockingScheduler
from aurora.tasks.jobs import ingest_local, ingest_rss_task, init_knowledge
from datetime import datetime
def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(init_knowledge.delay, "date", run_date=datetime.now())
    scheduler.add_job(ingest_local.delay, "interval", minutes=15, id="ingest_local")
    for i, url in enumerate(["https://hnrss.org/frontpage"]):
        scheduler.add_job(ingest_rss_task.delay, "interval", minutes=30, id=f"rss_{i}", args=[url])
    scheduler.start()
if __name__ == "__main__": main()
