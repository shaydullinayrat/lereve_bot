import time
import requests
import redis
from datetime import datetime, timedelta
from celery import shared_task

import json
# Настройка Redis
from core.settings import WB_API_TOKEN, WB_FEEDBACK_API_URL, FEEDBACK_REVIEW_DATE_CHECK_MINUTES, REDIS_HOST

# redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

# URL API Wildberries

HEADERS = {
    "Authorization": WB_API_TOKEN,
}

@shared_task
def fetch_feedbacks():
    # Формируем временные метки
    now = datetime.utcnow()
    date_from = int((now - timedelta(minutes=FEEDBACK_REVIEW_DATE_CHECK_MINUTES)).timestamp())
    date_to = int(now.timestamp())

    to_datetime = datetime(2023, 9, 15, 0, 0, 0)
    from_datetime = datetime(2020, 7, 19, 0, 0, 0)

    from_datetime_unix_timestamp = int(time.mktime(from_datetime.timetuple()))
    to_datetime_unix_timestamp = int(time.mktime(to_datetime.timetuple()))

    # date_from = from_datetime_unix_timestamp
    # date_to = to_datetime_unix_timestamp

    answered_params = {
        "isAnswered": "true",
        "take": 200,
        "skip": 0,
        "order": "dateDesc",
        "dateFrom": date_from,
        "dateTo": date_to,
    }
    # Запрос для отвеченных отзывов
    answered_response = requests.get(WB_FEEDBACK_API_URL, headers=HEADERS, params=answered_params)
    answered_feedbacks = answered_response.json().get("data", {}).get("feedbacks", [])

    # Небольшая задержка перед вторым запросом
    time.sleep(1)
    unanswered_params = {
        "isAnswered": "false",
        "take": 200,
        "skip": 0,
        "order": "dateDesc",
        "dateFrom": date_from,
        "dateTo": date_to,
    }
    # Запрос для неотвеченных отзывов
    unanswered_response = requests.get(WB_FEEDBACK_API_URL, headers=HEADERS, params=unanswered_params)
    unanswered_feedbacks = unanswered_response.json().get("data", {}).get("feedbacks", [])

    # Объединяем списки
    all_feedbacks = answered_feedbacks + unanswered_feedbacks


    # Формируем наш список `our_feedbacks`
    our_feedbacks = [
        {
            "article": feedback["productDetails"]["nmId"],
            "wb_username": feedback["userName"],
            "wb_feedback_id": feedback["id"],
            "text": feedback["text"],
            "review_date": feedback["createdDate"],
            "product_name": feedback["productDetails"]["productName"],
            "brand_name": feedback["productDetails"]["brandName"],
            "product_valuation": feedback["productValuation"],
        }
        for feedback in all_feedbacks
    ]

    # Сериализация перед сохранением
    redis_client.set('feedbacks', json.dumps(our_feedbacks))

