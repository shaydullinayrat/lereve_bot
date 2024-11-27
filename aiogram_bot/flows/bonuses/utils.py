import json
import time
from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async
from dateutil.parser import isoparse

from aiogram_bot.bot import bot

from aiogram_bot.flows.bonuses.keyboards import bonuses_keyboard, get_all_active_products_keyboard, numeric_keyboard, \
    send_phone_keyboard
from aiogram_bot.flows.bonuses.state_forms import ClientPhoneForm
from aiogram_bot.flows.bonuses.texts import no_active_bonus_text, my_feedback_not_exists, \
    no_feedback_for_product_in_hour
from aiogram_bot.flows.main_menu.keyboards import start_keyboard, back_to_main_menu_keyboard
from aiogram_bot.keyboards import generate_keyboard

from aiogram_bot.tasks import redis_client
from aiogram_bot.utils import send_callback_aiogram_message, format_date_iso_to_russian, send_message_aiogram_message
from apps.bonuses.models import Bonus, BonusRequest, Feedback
from apps.clients.models import Client
from apps.shops.models import Product
from core.settings import TELEGRAM_MANAGER_ID, TELEGRAM_MANAGER_USERNAME, FEEDBACK_REVIEW_DATE_CHECK_DAYS


@sync_to_async
def get_bonus_data(bonus_id):
    try:
        bonus = Bonus.objects.get(pk=bonus_id)
        text = f"<b>{bonus.title}</b>\n{bonus.description}"
        photo = None
        if bonus.photo:
            photo_path = bonus.photo.path  # Получаем путь к файлу
            photo = FSInputFile(photo_path)
        bonus_data = (text, photo, None)

        return bonus_data
    except:
        return None


async def show_bonus_list(callback, state):
    await callback.answer()
    await state.clear()

    # Извлекаем данные

    bonuses = await sync_to_async(lambda: list(Bonus.objects.filter(is_active=True)))()
    if len(bonuses) == 0:
        await send_callback_aiogram_message(
            callback=callback,
            text=no_active_bonus_text,
            keyboard=start_keyboard()
        )
    elif len(bonuses) == 1:
        bonus = bonuses[0]
        bonus_id = bonus.id
        await show_bonus(callback, bonus_id, back_button='start')

    else:
        await send_callback_aiogram_message(
            callback=callback,
            text='Выберите бонус',
            keyboard=await bonuses_keyboard()
        )


async def show_bonus(callback, bonus_id, back_button='start'):
    await callback.answer()
    await callback.message.edit_reply_markup()
    try:
        bonus = await Bonus.objects.aget(pk=bonus_id)

        if bonus:
            time_to_null_bonus = datetime.now() - timedelta(days=FEEDBACK_REVIEW_DATE_CHECK_DAYS)
            client_bonus_requests_count = await sync_to_async(
                lambda: BonusRequest.objects.filter(bonus=bonus,
                                                    client__user_id=callback.from_user.id,
                                                    created_at__gte=time_to_null_bonus
                                                    ).count())()

            if client_bonus_requests_count > 0:
                await callback.message.answer(
                    text=f'<b>Вы уже воспользовались данной бонусной программой </b>. \n\nПовторно в ней участовать можно будет через <b> {FEEDBACK_REVIEW_DATE_CHECK_DAYS} дней</b> после первого участия',
                    reply_markup=start_keyboard()
                )
            else:
                bonus_text = f'<b>{bonus.title}</b> \n {bonus.description}'

                buttons_data = [
                    ("Назад", back_button),
                    ("Участвую!", f"participate_bonus__{bonus_id}"),
                ]
                keyboard = generate_keyboard(buttons_data, [2])
                if bonus.photo:
                    photo_path = bonus.photo.path  # Получаем путь к файлу
                    photo = FSInputFile(photo_path)
                    await callback.message.answer_photo(
                        photo=photo,
                        caption=bonus_text,
                        reply_markup=keyboard
                    )
                else:
                    await callback.message.answer(
                        text=bonus_text,
                        reply_markup=keyboard
                    )

    except:
        await send_callback_aiogram_message(callback=callback,
                                            text='К сожалению нет активных бонусов',
                                            keyboard=back_to_main_menu_keyboard())


async def show_product_feedbacks(callback, state, data):
    await callback.answer()
    await callback.message.edit_reply_markup()
    data = data.split('|')
    bonus_id = int(data[0].split(':')[1])
    article = int(data[1].split(':')[1])

    wb_feedbacks = json.loads(redis_client.get('feedbacks'))

    wb_feedback_id_list = await sync_to_async(lambda: list(Feedback.objects.values_list('wb_feedback_id', flat=True)))()

    # Фильтрация списка
    filtered_feedbacks = [item for item in wb_feedbacks if
                          item['article'] == article
                          and item['product_valuation'] == 5
                          and item['wb_feedback_id'] not in wb_feedback_id_list
                          and item['text'].lower().startswith("супер")
                          ]

    if filtered_feedbacks:
        # review_date
        for feedback in filtered_feedbacks:
            wb_username = feedback.get('wb_username')
            wb_feedback_id = feedback.get('wb_feedback_id')
            review_date = feedback.get('review_date')
            review_date = format_date_iso_to_russian(review_date)
            product_valuation = feedback.get('product_valuation')
            product_name = feedback.get('product_name')
            text = feedback.get('text')

            text = f'<b>{wb_username}:</b> {product_valuation} ★ \n  {product_name} \n  {review_date} \n \n<i>{text}</i>'
            callback_data = f'reg_fb__bonus_id:{bonus_id}|article:{article}|fb_id:{wb_feedback_id}'
            buttons_data = [
                ("Это мой отзыв!", callback_data),
            ]
            layout = [1]
            keyboard = generate_keyboard(buttons_data, layout)

            sent_message = await callback.message.answer(
                text=text,
                reply_markup=keyboard
            )
            data = await state.get_data()
            message_ids = data.get("message_ids", [])
            message_ids.append(sent_message.message_id)
            await state.update_data(message_ids=message_ids)

        buttons_data = [
            ("Назад", f"bonus_{bonus_id}"),
        ]
        keyboard = generate_keyboard(buttons_data, [1])

        sent_message = await callback.message.answer(
            text=my_feedback_not_exists,
            reply_markup=keyboard
        )
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)

    else:
        buttons_data = [
            ("Назад", f"bonus_{bonus_id}"),
        ]

        await send_callback_aiogram_message(
            callback=callback,
            text=no_feedback_for_product_in_hour,
            keyboard=generate_keyboard(buttons_data, [1])
        )


async def participate_bonus(callback, state, bonus_id):
    await callback.answer()
    await callback.message.edit_reply_markup()
    try:

        keyboard = await get_all_active_products_keyboard(bonus_id)
        sent_message = await callback.message.answer(
            text='<b>Благодарим за высокую оценку нашего товара!</b> \nВыберите тот <b>продукт</b>, который вы приобрели. \n\nДалее <b>выберите Ваш отзыв</b>, который вы оставили на данный продукт:',
            reply_markup=keyboard
        )
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)


    except:
        await send_callback_aiogram_message(
            callback=callback,
            text='К сожалению нет активных бонусов',
            keyboard=back_to_main_menu_keyboard()
        )


@sync_to_async
def validate_feedback(user_id, bonus_id, article, wb_feedback_id):
    client = Client.objects.get(user_id=user_id)
    product = Product.objects.get(article=article)
    feedbacks = json.loads(redis_client.get('feedbacks'))
    feedback_item = next((item for item in feedbacks if item['wb_feedback_id'] == wb_feedback_id), None)

    if feedback_item:
        is_there_same_feedback = Feedback.objects.filter(wb_feedback_id=wb_feedback_id).exists()
        if is_there_same_feedback:
            return 'same_feedback_exists'

        current_datetime = datetime.now()
        check_time = current_datetime - timedelta(days=FEEDBACK_REVIEW_DATE_CHECK_DAYS)
        is_there_other_feedback_from_client = Feedback.objects.filter(product=product,
                                                                      bonus_request__client=client,
                                                                      review_date__gte=check_time
                                                                      ).exists()
        if is_there_other_feedback_from_client:
            return 'same_client_feedback_exists'

        return f'feedbacks_can_register'

    return 'no_feedbacks_in_wb'


# Функция для удаления нескольких сообщений
async def delete_previous_messages(message: Message, state: FSMContext):
    data = await state.get_data()

    message_ids = data.get("message_ids", [])

    for msg_id in message_ids:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
        except Exception:
            pass  # Игнорируем ошибки
    await state.update_data(message_ids=[])


async def register_feedback(callback, state, data):

    data = data.split('|')
    bonus_id = int(data[0].split(':')[1])
    article = int(data[1].split(':')[1])
    wb_feedback_id = data[2].split(':')[1]
    user_id = callback.from_user.id

    await state.update_data(bonus_id=bonus_id)
    await state.update_data(article=article)
    await state.update_data(wb_feedback_id=wb_feedback_id)
    await state.update_data(user_id=user_id)

    result = await validate_feedback(user_id, bonus_id, article, wb_feedback_id)

    await delete_previous_messages(message=callback.message, state=state)
    time.sleep(0.5)

    if result == 'same_feedback_exists':

        print('result ', result)
        await callback.message.answer(
            text='К сожалению, этот отзыв уже использован для бонусной программы',
            reply_markup=back_to_main_menu_keyboard()
        )
    elif result == 'same_client_feedback_exists':
        await callback.message.answer(
            text=f'<b>Вы уже воспользовались бонусной программой. </b>\n\n'
                 f'Повторно участвовать можно будет только <b> через {FEEDBACK_REVIEW_DATE_CHECK_DAYS} дней </b>',
            reply_markup=back_to_main_menu_keyboard()
        )
    elif result.startswith('feedbacks_can_register'):

        # Клавиатура с запросом телефона




        await callback.message.answer(
            "Поздравляем! Остался последний шаг. \n\nОтправьте пожалуйста свой <b>номер телефона </b>, на который вы бы хотели <b>получить бонус</b>, нажав на кнопку \n\n                        <b> НИЖЕ ↓↓↓ </b>",
        reply_markup=send_phone_keyboard)
        await state.set_state(ClientPhoneForm.phone)


@sync_to_async
def create_bonus_request(message, data):
    phone = data.get("phone")
    bonus_id = data.get("bonus_id")
    article = data.get("article")
    wb_feedback_id = data.get('wb_feedback_id')
    user_id = message.from_user.id
    client = Client.objects.get(user_id=user_id)
    product = Product.objects.get(article=article)
    feedbacks = json.loads(redis_client.get('feedbacks'))
    feedback_item = next((item for item in feedbacks if item['wb_feedback_id'] == wb_feedback_id), None)
    if feedback_item:
        bonus_request = BonusRequest.objects.create(
            client=client,
            bonus_id=bonus_id,
            product=product,
            status='submitted',
            phone=phone
        )
        client.phone_number = phone
        client.wb_username = feedback_item['wb_username']
        client.save()

        feedback = Feedback.objects.create(
            product=product,
            bonus_request=bonus_request,
            wb_feedback_id=feedback_item['wb_feedback_id'],
            wb_username=feedback_item['wb_username'],
            text=feedback_item['text'],
            review_date=isoparse(feedback_item['review_date']),
        )

        return bonus_request.bonus.title
    return None


async def register_bonus_request(message, state):
    data = await state.get_data()
    bonus_title = await create_bonus_request(message, data)
    if bonus_title:
        manager_chat_id = TELEGRAM_MANAGER_ID  # Укажите реальный chat_id менеджера
        manager_username = TELEGRAM_MANAGER_USERNAME  # Укажите реальный chat_id менеджера
        user_info = f"Пользователь: @{message.from_user.username} (ID: {message.from_user.id})"

        await bot.send_message(manager_chat_id,
                               f"{user_info} хочет учавствовать в бонусной программе: {bonus_title}, телефон: {data.get('phone')}")

        await send_message_aiogram_message(
            message,
            'Поздравляем! Ваша заявка зарегистрирована. \n\nВ ближайшее время с вами свяжется наш администратор для перечисления денег',
            start_keyboard()
        )
    else:
        await send_message_aiogram_message(
            message, 'Произошла ошибка. Попробуйте сначала', start_keyboard()
        )
