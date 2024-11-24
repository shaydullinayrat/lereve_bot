from aiogram_bot import main
# from aiogram_bot.services.send_message import send_callback_aiogram_message
from aiogram_bot.flows.main_menu.keyboards import start_keyboard, back_to_main_menu_keyboard
from aiogram_bot.utils import send_callback_aiogram_message, send_message_aiogram_message
from core.settings import TELEGRAM_MANAGER_ID, TELEGRAM_MANAGER_USERNAME



async def show_care_service(callback, state):
    await callback.answer()
    await state.clear()

    manager_chat_id = TELEGRAM_MANAGER_ID  # Укажите реальный chat_id менеджера
    manager_username = TELEGRAM_MANAGER_USERNAME  # Укажите реальный chat_id менеджера
    user_info = f"Пользователь: @{callback.from_user.username} (ID: {callback.from_user.id})"

    await main.bot.send_message(manager_chat_id, f"{user_info} хочет с вами связаться.")

    text = f"Мы уведомили менеджера. Вы можете написать ему напрямую: @{manager_username}"

    await send_callback_aiogram_message(
        callback=callback,
        text=text,
        keyboard=back_to_main_menu_keyboard()
    )