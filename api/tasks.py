from celery import shared_task

@shared_task
def offboarding_task(message):
    print(message)