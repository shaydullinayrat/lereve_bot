from aiogram_bot import main
from aiogram_bot.flows.care_service.keyboards import get_all_active_products_care_keyboard
from aiogram_bot.flows.care_service.texts import user_written_to_care_service_text, \
    manager_notified_text, user_to_care_product_text
from aiogram_bot.flows.main_menu.keyboards import back_to_main_menu_keyboard
from aiogram_bot.utils import send_callback_aiogram_message
from apps.shops.models import Product
from core.settings import TELEGRAM_CARE_SERVICE_ID, \
    TELEGRAM_CARE_SERVICE_USERNAME


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

async def send_message_to_care_service(callback, product_id):
    await callback.answer()
    product = await Product.objects.aget(id=product_id)
    care_service_id = TELEGRAM_CARE_SERVICE_ID  # Укажите реальный chat_id менеджера
    care_service_username = TELEGRAM_CARE_SERVICE_USERNAME  # Укажите реальный chat_id менеджера
    text = user_to_care_product_text.format(
        callback.from_user.username, callback.from_user.id, product.title, product.article, product.url
    )
    await main.bot.send_message(care_service_id, text)
    text = manager_notified_text.format(care_service_username)
    await send_callback_aiogram_message(
        callback=callback,
        text=text,
        keyboard=back_to_main_menu_keyboard()
    )
