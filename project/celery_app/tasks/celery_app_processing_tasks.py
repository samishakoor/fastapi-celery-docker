import time
from celery_app.celery import celery_app


@celery_app.task(
    bind=True,
    name="create_task",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 60},
    retry_backoff=True,
    soft_time_limit=600,  # 10 minutes soft limit
    time_limit=900,  # 15 minutes hard limit
    max_memory_per_child=300000,  # 300MB per child process
    # Removed rate_limit to allow unlimited queuing
)
def create_task(self, task_type):
    time.sleep(int(task_type) * 10)
    return True
