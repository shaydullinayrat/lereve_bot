from aiogram_bot import main
from aiogram_bot.flows.main_menu.keyboards import back_to_main_menu_keyboard
from aiogram_bot.utils import send_callback_aiogram_message
from core.settings import TELEGRAM_CARE_SERVICE_ID, \
    TELEGRAM_CARE_SERVICE_USERNAME


async def show_care_service(callback, state):
    await callback.answer()
    await state.clear()

    care_service_id = TELEGRAM_CARE_SERVICE_ID  # Укажите реальный chat_id менеджера
    care_service_username = TELEGRAM_CARE_SERVICE_USERNAME  # Укажите реальный chat_id менеджера
    user_info = f"Пользователь: @{callback.from_user.username} (ID: {callback.from_user.id})"

    await main.bot.send_message(care_service_id, f"{user_info} хочет с вами связаться.")

    text = f"Мы уведомили менеджера. Вы можете написать ему напрямую: @{care_service_username}"

    await send_callback_aiogram_message(
        callback=callback,
        text=text,
        keyboard=back_to_main_menu_keyboard()
    )
