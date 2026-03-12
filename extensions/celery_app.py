from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "auth_tasks",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
)

celery.conf.update(
    task_serializer = "json",
    accept_content = ["json"],
    result_serializer = "json",
    timezone="UTC",
    enable_utc = True
)

celery.conf.task_routes = {
    "tasks.email_tasks.*":{"queue":"email_queue"}
}

import tasks.email_tasks