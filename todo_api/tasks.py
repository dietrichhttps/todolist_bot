from celery import shared_task
from django.utils import timezone
from .models import Task
from todolist.celery import celery_app

@celery_app.task
def send_task_reminder(task_id):
    from django.conf import settings
    from telegram_bot.bot import send_telegram_notification
    try:
        task = Task.objects.get(id=task_id)
        if task.due_date and not task.is_completed:
            message = f"Напоминание: задача '{task.title}' должна быть выполнена к {task.due_date}"
            send_telegram_notification(task.user_id, message)
    except Task.DoesNotExist:
        pass

@celery_app.task
def check_pending_tasks():
    now = timezone.now()
    pending_tasks = Task.objects.filter(
        due_date__lte=now + timezone.timedelta(hours=1),
        is_completed=False
    )
    for task in pending_tasks:
        send_task_reminder.delay(task.id)