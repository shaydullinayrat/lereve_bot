from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async

from aiogram_bot.flows.care_service import texts
from aiogram_bot.flows.care_service.keyboards import get_all_active_products_care_keyboard
from aiogram_bot.flows.care_service.texts import user_to_care_product_text
from aiogram_bot.flows.main_menu.keyboards import back_to_main_menu_keyboard, start_keyboard

from aiogram_bot.keyboards import generate_keyboard
from aiogram_bot.utils import send_callback_aiogram_message, send_message_aiogram_message
from apps.care_requests.models import CareRequest, CareRequestDetail
from apps.clients.models import Client
from apps.shops.models import Product
from core.settings import TELEGRAM_CARE_SERVICE_ID, \
    TELEGRAM_CARE_SERVICE_USERNAME
from django.db import transaction

from aiogram_bot.bot import bot


async def get_file_url(file_id: str) -> str:
    file = await bot.get_file(file_id)
    return f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"


class SupportState(StatesGroup):
    select_product = State()
    describe_issue = State()
    confirm_request = State()


async def show_care_service(callback, state):
    await callback.answer()
    await state.clear()

    keyboard = await get_all_active_products_care_keyboard()
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.сhoose_product_text,
        keyboard=keyboard
    )


async def send_message_to_care_service(callback, state, product_id):
    await callback.answer()
    product = await Product.objects.aget(id=product_id)
    await state.update_data(product_id=product_id)
    await state.update_data(product_article=product.article)
    await state.update_data(product_url=product.url)
    await state.update_data(product_title=product.title)
    await state.set_state(SupportState.describe_issue)


    button_data = [
        ('Отмена', 'care_service')
    ]

    await send_callback_aiogram_message(
        callback=callback,
        text=texts.write_problems_text.format(product.url, product.title, product.article),
        keyboard=generate_keyboard(button_data, [1]),
        # disable_web_page_preview=True

    )


@sync_to_async
def create_client_request(data):
    care_request_id = data['care_request_id']
    with transaction.atomic():
        client = Client.objects.get(user_id=data['client_id'])
        if not care_request_id:
            care_request = CareRequest.objects.create(
                client=client,
                product_id=data['product_id'],
            )
        else:
            care_request = CareRequest.objects.get(id=care_request_id)

        CareRequestDetail.objects.create(
            care_request=care_request,
            media_type=data['media_type'],
            file_id=data['file_id'],
            file_url=data['file_url'],
            text=data['text'],
        )
    return care_request.id


async def get_client_request(message, state):
    data = await state.get_data()
    product_id = data.get("product_id")
    care_request_id = data.get("care_request_id")
    client_id = message.from_user.id
    text = None
    media_type = None
    file_id = None
    file_url = None
    if message.text:
        media_type = "text"
        text = message.text
    elif message.photo:
        media_type = "photo"
        file_id = message.photo[-1].file_id
        file_url = await get_file_url(file_id)
    elif message.video:
        media_type = "video"
        file_id = message.video.file_id
        file_url = await get_file_url(file_id)
    elif message.audio:
        media_type = "audio"
        file_id = message.audio.file_id
        file_url = await get_file_url(file_id)
    elif message.voice:
        media_type = "voice"
        file_id = message.voice.file_id
        file_url = await get_file_url(file_id)

    request_data = {
        'client_id': client_id,
        'product_id': product_id,
        'media_type': media_type,
        'file_id': file_id,
        'file_url': file_url,
        'text': text,
        'care_request_id': care_request_id,

    }
    # Сохраняем данные в базу
    care_request_id = await create_client_request(request_data)
    await state.update_data(care_request_id=care_request_id)

    data = await state.get_data()
    messages = data.get("messages", [])
    messages.append(message.message_id)

    # Обновляем данные состояния

    await state.update_data(messages=messages)

    await state.update_data(care_request_id=care_request_id)

    await send_message_aiogram_message(message=message,
                                       text=texts.request_detail_text,
                                       keyboard=generate_keyboard([('Закончить запрос', 'finish_request')], [1]))



async def finish_request(callback, state):
    data = await state.get_data()
    client_id = callback.from_user.id
    messages_to_forward = data.get("messages", [])

    if not messages_to_forward:
        # Уведомляем пользователя
        await send_callback_aiogram_message(
            callback=callback,
            text=texts.no_text_to_send_text,
            keyboard=back_to_main_menu_keyboard()
        )

        await state.clear()
        return

    await callback.message.reply_photo(
        photo=FSInputFile("staticfiles/notified_manager_photo.jpeg"),
        caption=texts.care_service_connect_you_text,
        reply_markup=back_to_main_menu_keyboard()
    )

    try:
        # Отправляем админу уведомление о новом запросе
        await bot.send_message(
            TELEGRAM_CARE_SERVICE_ID,
            text=user_to_care_product_text.format(callback.from_user.username,
                                                  callback.from_user.id,
                                                  data.get('product_url'),
                                                  data.get('product_title'),
                                                  data.get('product_article'),
                                                  ),
        )

        # Пересылаем сообщения админу
        for msg_id in messages_to_forward:
            await bot.forward_message(
                chat_id=TELEGRAM_CARE_SERVICE_ID,
                from_chat_id=client_id,
                message_id=msg_id,
            )


        await state.clear()

    except Exception as e:
        await send_callback_aiogram_message(
            callback=callback,
            text=texts.request_error_text,
            keyboard=back_to_main_menu_keyboard()
        )
        await state.clear()
        raise e
