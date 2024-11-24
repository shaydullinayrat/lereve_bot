import asyncio

import requests
from datetime import datetime, timedelta

from aiogram.client.session import aiohttp

FEEDBACK_API_URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
WB_API_TOKEN = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQxMTE4djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc0Nzk4NDE3MiwiaWQiOiIwMTkzNTAyMS0zMDFiLTdmMTktOTIxZC04OTM1YTBkMjVlNmMiLCJpaWQiOjIzMDc5MDM0LCJvaWQiOjg1MTY4LCJzIjo3OTM0LCJzaWQiOiI5NzdjODVkZC04ZGZjLTU4MGQtODU5Mi0yMGM3ZmQ5ZGRlZWYiLCJ0IjpmYWxzZSwidWlkIjoyMzA3OTAzNH0.GuYZF4tq--_6TLXYR7S-gdueHWcvz3hWY6-s9fNctFgazbZsJykZWVpsiWrYfE3146jDODSjkDYLwC1UYSbjOg'

import time
TEST_NMID = 54431466
# Пример использования
from datetime import datetime


def datetime_to_unix_timestamp(dt_object):
    """
    Преобразует объект datetime в Unix timestamp.

    :param dt_object: Объект datetime.
    :return: Unix timestamp (int).
    """
    if not isinstance(dt_object, datetime):
        raise TypeError("Аргумент должен быть объектом datetime.")

    # Преобразование в Unix timestamp
    unix_timestamp = int(time.mktime(dt_object.timetuple()))
    return unix_timestamp


def get_current_unix_timestamp():
    """
    Возвращает текущую дату и время в формате Unix timestamp.
    """
    current_time = datetime.now()
    unix_timestamp = int(time.mktime(current_time.timetuple()))
    return unix_timestamp

async def fetch_feedbacks(is_answered: bool, date_from: int, date_to: int, nm_id: int):
    """
    Отправляет GET-запрос на API с параметром isAnswered.
    :param is_answered: Значение параметра isAnswered (True или False).
    :return: JSON-ответ от API.
    """

    headers = {
        "Authorization": WB_API_TOKEN,
    }
    params = {
        "isAnswered": str(is_answered).lower(),
        'take': 200,
        'skip': 0,
        'order': 'dateDesc',
        'dateFrom': date_from,
        'dateTo': date_to,
        'nmId': nm_id,


    }  # API ожидает true/false в виде строки
    async with aiohttp.ClientSession() as session:
        async with session.get(FEEDBACK_API_URL, params=params, headers=headers, timeout=10) as response:
            response.raise_for_status()  # Проверка на HTTP ошибки
            return await response.json()


async def get_combined_feedbacks(dateFrom: int, dateTo: int, nmId: int):
    """
    Делает два запроса к API, объединяет ответы и возвращает суммарный результат.
    """
    # Первый запрос с isAnswered=true
    feedbacks_true = await fetch_feedbacks(is_answered=True, date_from=dateFrom, date_to=dateTo, nm_id=nmId)

    feedbacks_true_data = feedbacks_true.get('data', None).get('feedbacks', None)

    # Пауза в 1 секунду
    await asyncio.sleep(1)

    # Второй запрос с isAnswered=false
    feedbacks_false = await fetch_feedbacks(is_answered=False, date_from=dateFrom, date_to=dateTo, nm_id=nmId)
    feedbacks_false_data = feedbacks_false.get('data', None).get('feedbacks', None)
    # Объединение результатов
    combined_feedbacks = feedbacks_true_data + feedbacks_false_data

    print('combined_feedbacks ', combined_feedbacks)

    return combined_feedbacks

async def get_recent_comments(article):
    # URL для запросов

    current_time = datetime.now()
    to_datetime = datetime(2023, 9, 15, 0, 0, 0)
    from_datetime = datetime(2023, 7, 19, 0, 0, 0)

    from_datetime_unix_timestamp = int(time.mktime(from_datetime.timetuple()))
    to_datetime_unix_timestamp = int(time.mktime(to_datetime.timetuple()))
    unix_timestamp = int(time.mktime(current_time.timetuple()))

    await get_combined_feedbacks(from_datetime_unix_timestamp, to_datetime_unix_timestamp, article)

    get_params = f'?isAnswered=true&take=200&skip=0&order=dateDesc&dateFrom={from_datetime_unix_timestamp}&dateTo={to_datetime_unix_timestamp}&nmId={article}'
    url = f"{FEEDBACK_API_URL}{get_params}"

    print('url ', url)
    headers = {
        "Authorization": WB_API_TOKEN,
    }
    return None

    try:

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", None)

        print('data ', data)
        if data is not None:
            feedbacks = data['feedbacks']

        # response = requests.get(url, timeout=10)  # Таймаут 10 секунд
        # response.raise_for_status()  # Если произошла ошибка, выбросится исключение
        #
        # feedbacks = response.json().get("data", [])
        # if not feedbacks:
        #     return "Отзывы отсутствуют."

        # now = datetime.utcnow()
        # one_hour_ago = now - timedelta(hours=1)
        #
        # # Фильтруем отзывы за последний час
        # recent_feedbacks = [
        #     f"Автор: {feedback['user']['name']}\n"
        #     f"Оценка: {feedback['productValuation']}\n"
        #     f"Комментарий: {feedback['text']}\n"
        #     f"Дата: {feedback['createdDate']}"
        #     for feedback in feedbacks
        #     if datetime.fromisoformat(feedback['createdDate'].replace("Z", "+00:00")) >= one_hour_ago
        # ]
        #
        # if not recent_feedbacks:
        #     return "За последний час отзывов не найдено."

        return data
    except requests.exceptions.RequestException as e:
        return f"Ошибка при получении отзывов: {e}"
