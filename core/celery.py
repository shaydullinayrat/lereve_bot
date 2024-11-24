from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Указываем настройки Django
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Создаем экземпляр Celery
app = Celery('core')

print('Celery app ', app)

app.conf.beat_schedule = {
    'fetch_feedbacks-every-minute': {
        'task': 'aiogram_bot.tasks.fetch_feedbacks',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
}

# Загружаем настройки из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')
# from django.conf:settings
# Автоматически обнаруживаем задачи в `tasks.py`
app.autodiscover_tasks(['aiogram_bot'])
# @app.task
# def check_celery_settings():
#     # Выводим некоторые настройки Celery
#     print("Celery Broker URL: ", app.conf.broker_url)
#     print("Celery Timezone: ", app.conf.timezone)
#     print("Celery Accept Content: ", app.conf.accept_content)
