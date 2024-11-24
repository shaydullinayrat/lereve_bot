import time
import requests
import redis
from datetime import datetime, timedelta
from celery import shared_task

# Настройка Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# URL API Wildberries
WB_URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
WB_API_TOKEN = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQxMTE4djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc0Nzk4NDE3MiwiaWQiOiIwMTkzNTAyMS0zMDFiLTdmMTktOTIxZC04OTM1YTBkMjVlNmMiLCJpaWQiOjIzMDc5MDM0LCJvaWQiOjg1MTY4LCJzIjo3OTM0LCJzaWQiOiI5NzdjODVkZC04ZGZjLTU4MGQtODU5Mi0yMGM3ZmQ5ZGRlZWYiLCJ0IjpmYWxzZSwidWlkIjoyMzA3OTAzNH0.GuYZF4tq--_6TLXYR7S-gdueHWcvz3hWY6-s9fNctFgazbZsJykZWVpsiWrYfE3146jDODSjkDYLwC1UYSbjOg'

HEADERS = {
    "Authorization": WB_API_TOKEN,
}

@shared_task
def fetch_feedbacks():
    # Формируем временные метки
    now = datetime.utcnow()
    date_from = int((now - timedelta(hours=1)).timestamp())
    date_to = int(now.timestamp())

    to_datetime = datetime(2023, 9, 15, 0, 0, 0)
    from_datetime = datetime(2023, 7, 19, 0, 0, 0)

    from_datetime_unix_timestamp = int(time.mktime(from_datetime.timetuple()))
    to_datetime_unix_timestamp = int(time.mktime(to_datetime.timetuple()))

    date_from = from_datetime_unix_timestamp
    date_to = to_datetime_unix_timestamp

    # Запрос для отвеченных отзывов
    answered_url = f"{WB_URL}?isAnswered=true&take=200&skip=0&order=dateDesc&dateFrom={date_from}&dateTo={date_to}"
    answered_response = requests.get(answered_url, headers=HEADERS)
    answered_feedbacks = answered_response.json().get("data", {}).get("feedbacks", [])

    # Небольшая задержка перед вторым запросом
    time.sleep(1)

    # Запрос для неотвеченных отзывов
    unanswered_url = f"{WB_URL}?isAnswered=false&take=200&skip=0&order=dateDesc&dateFrom={date_from}&dateTo={date_to}"
    unanswered_response = requests.get(unanswered_url, headers=HEADERS)
    unanswered_feedbacks = unanswered_response.json().get("data", {}).get("feedbacks", [])

    # Объединяем списки
    all_feedbacks = answered_feedbacks + unanswered_feedbacks

    # Формируем наш список `our_feedbacks`
    our_feedbacks = [
        {
            "article": feedback["productDetails"]["nmId"],
            "wb_username": feedback["userName"],
            "wb_id": feedback["id"],
            "text": feedback["text"],
            "review_date": feedback["createdDate"]
        }
        for feedback in all_feedbacks
    ]

    # Сохраняем в Redis
    import json

    # Сериализация перед сохранением
    redis_client.set('feedbacks', json.dumps(our_feedbacks))

