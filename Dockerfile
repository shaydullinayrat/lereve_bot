# Используем официальный Python образ в качестве базового
FROM python:3.9-alpine3.16

# Установим переменную окружения для предотвращения вопросов при установке пакетов
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /lereve_app

# Копируем зависимости
COPY requirements.txt /temp/requirements.txt

RUN apk add postgresql-client build-base postgresql-dev

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /temp/requirements.txt

# Копируем все файлы в контейнер
COPY . /lereve_app

# Открываем порты (если нужно для Django или других сервисов)
EXPOSE 8000

RUN adduser --disabled-password lereve-user

USER lereve-user
# Настроим запуск для Django, Celery и Celery Beat
#CMD ["sh", "-c", "celery -A core worker --loglevel=info & celery -A core beat --loglevel=info & python manage.py runserver 0.0.0.0:8000 & python manage.py runbot"]
