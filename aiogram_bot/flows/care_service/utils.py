from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async
from django.db.models import Prefetch

from aiogram_bot import main
from aiogram_bot.flows.care_service.keyboards import get_all_active_products_care_keyboard
from aiogram_bot.flows.care_service.texts import user_written_to_care_service_text, \
    manager_notified_text, user_to_care_product_text
from aiogram_bot.flows.main_menu.keyboards import back_to_main_menu_keyboard, start_keyboard
from aiogram_bot.flows.main_menu.utils import get_welcome_photo
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

    care_service_id = TELEGRAM_CARE_SERVICE_ID  # Укажите реальный chat_id менеджера
    care_service_username = TELEGRAM_CARE_SERVICE_USERNAME  # Укажите реальный chat_id менеджера
    text = user_written_to_care_service_text.format(callback.from_user.username, callback.from_user.id)
    # await main.bot.send_message(care_service_id, text)

    text = manager_notified_text.format(care_service_username)

    text = "Пожалуйста, выберите продукт, который вы приобрели и по которому у вас возникли вопросы или проблемы."

    keyboard = await get_all_active_products_care_keyboard()
    await send_callback_aiogram_message(
        callback=callback,
        text=text,
        keyboard=keyboard
    )


async def send_message_to_care_service(callback, state, product_id):
    await callback.answer()
    product = await Product.objects.aget(id=product_id)
    care_service_id = TELEGRAM_CARE_SERVICE_ID  # Укажите реальный chat_id менеджера
    care_service_username = TELEGRAM_CARE_SERVICE_USERNAME  # Укажите реальный chat_id менеджера
    text = user_to_care_product_text.format(
        callback.from_user.username, callback.from_user.id, product.title, product.article, product.url
    )
    # await state.set_state(SupportState.select_product)
    await state.update_data(product_id=product_id)
    await state.set_state(SupportState.describe_issue)

    text = 'Вы покупали у нас продукт: <b>{}</b>. \nОпишите пожалуйста какие сложности у вас возникли с продуктом, вместе с  <b>описанием</b>, можете прикрепить <b> фотографию</b>'. \
        format(product.title)

    button_data = [
        ('Отмена', 'care_service')
    ]
    await send_callback_aiogram_message(
        callback=callback,
        text=text,
        keyboard=generate_keyboard(button_data, [1])

    )

    await main.bot.send_message(care_service_id, text)
    # text = manager_notified_text.format(care_service_username)
    # await send_callback_aiogram_message(
    #     callback=callback,
    #     text=text,
    #     keyboard=back_to_main_menu_keyboard()
    # )


@sync_to_async
def create_client_request(data):
    print('data sfs ', data)
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
    product_id = data["product_id"]
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

    keyboard = generate_keyboard(
        [
            ('Закончить запрос', 'finish_request')
        ], [1]
    )
    text = "Сообщение сохраненно. Вы можете отправить еще <b> сообщение с текстом, фото или видео </b> для дополнения своего запроса, или нажать <b>кнопку: Закончить запрос</b>."
    await send_message_aiogram_message(message=message,
                                       text=text,
                                       keyboard=keyboard)


@sync_to_async
def generate_admin_message(callback, care_request_id):
    care_request = CareRequest.objects.prefetch_related(
        Prefetch("details")
    ).get(id=care_request_id)

    admin_message = f"📩 **Новый запрос в поддержку**\n\n"
    admin_message += f"👤 Клиент: {callback.from_user.full_name} (ID: {callback.from_user.id})\n"
    admin_message += f"📦 Продукт: {care_request.product}\n"
    admin_message += f"🕒 Создан: {care_request.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    details = care_request.details.all()
    if details.exists():
        admin_message += "\n📎 Вложения:\n"
        for detail in details:
            admin_message += f"- **Тип**: {detail.media_type}\n"
            if detail.file_url:
                admin_message += f"  [Открыть файл]({detail.file_url})\n"
            if detail.text:
                admin_message += f"  Описание: {detail.text}\n"
            admin_message += "\n"
            # Отправляем сообщение администратору

    return admin_message


async def finish_request(callback, state):
    data = await state.get_data()
    care_request_id = data.get('care_request_id')
    print('care_request ', care_request_id)

    # admin_message = await generate_admin_message(callback, care_request_id)
    # await bot.send_message(
    #     TELEGRAM_CARE_SERVICE_ID,
    #     admin_message,
    #     parse_mode="Markdown",
    #     disable_web_page_preview=True,
    # )

    client_id = callback.from_user.id
    messages_to_forward = data.get("messages", [])

    if not messages_to_forward:
        # Уведомляем пользователя
        await send_callback_aiogram_message(
            callback=callback,
            text='Нет сообщений для пересылки. Пожалуйста, начните заново.',
            keyboard=back_to_main_menu_keyboard()
        )

        # await callback.reply("Нет сообщений для пересылки. Пожалуйста, начните заново.")
        await state.clear()
        return

    await callback.message.reply_photo(
        photo=FSInputFile("staticfiles/notified_manager_photo.jpeg"),
        caption='Ваш запрос принят и отправлен <b>менеджеру</b>. В ближайшее время он <b>свяжется с вами</b>',
        reply_markup=start_keyboard()
    )

    try:
        # Отправляем админу уведомление о новом запросе
        await bot.send_message(
            TELEGRAM_CARE_SERVICE_ID,
            f"📩 Новый запрос на тех поддержку от клиента <b>{callback.from_user.full_name}</b> (ID: {client_id}). по продукту:",
        )

        # Пересылаем сообщения админу
        for msg_id in messages_to_forward:
            await bot.forward_message(
                chat_id=TELEGRAM_CARE_SERVICE_ID,
                from_chat_id=client_id,
                message_id=msg_id,
            )

        await bot.send_message(
            TELEGRAM_CARE_SERVICE_ID,
            f"📩 Новый запрос на тех поддержку от клиента <b>{callback.from_user.full_name}</b> (ID: {client_id}). по продукту:",
        )



        # Уведомляем пользователя
        # await send_callback_aiogram_message(
        #     callback=callback,
        #     text='Ваш запрос принят и отправлен <b>менеджеру</b>. В ближайшее время он <b>свяжется с вами</b>',
        #     keyboard=back_to_main_menu_keyboard()
        # )

        await state.clear()

    except Exception as e:
        await send_callback_aiogram_message(
            callback=callback,
            text='Произошла ошибка при отправке запроса. Пожалуйста, попробуйте еще раз',
            keyboard=back_to_main_menu_keyboard()
        )
        await state.clear()
        raise e
