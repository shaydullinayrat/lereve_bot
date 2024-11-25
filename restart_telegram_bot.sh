#!/bin/bash

# Имя контейнера и сервиса в docker-compose
CONTAINER_NAME="telegram-bot"
SERVICE_NAME="telegram-bot"

# Удаление контейнера (если существует)
echo "Удаляем контейнер $CONTAINER_NAME..."
docker rm -f $CONTAINER_NAME 2>/dev/null || echo "Контейнер $CONTAINER_NAME не найден."

# Пересборка образа
echo "Пересборка образа для сервиса $SERVICE_NAME..."
docker-compose build $SERVICE_NAME

# Запуск нового контейнера
echo "Запускаем контейнер $SERVICE_NAME..."
docker-compose up -d $SERVICE_NAME

echo "Готово!"
