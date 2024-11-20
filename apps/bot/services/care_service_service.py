
# Главное меню
from apps.bot.bot import bot
from apps.bot.services.main_menu_service import create_main_menu_buttons_markup
from core.settings import TELEGRAM_MANAGER_ID, TELEGRAM_MANAGER_USERNAME


async def send_care_service_message(call):
    """
        Обработчик кнопки 'Служба заботы'.
       Уведомляет менеджера и предоставляет пользователю ссылку.
    """

    await bot.answer_callback_query(call.id)

    # Уведомление менеджера
    manager_chat_id = TELEGRAM_MANAGER_ID  # Укажите реальный chat_id менеджера
    manager_username = TELEGRAM_MANAGER_USERNAME  # Укажите реальный chat_id менеджера
    user_info = f"Пользователь: @{call.from_user.username} (ID: {call.from_user.id})"
    await bot.send_message(manager_chat_id, f"{user_info} хочет с вами связаться.")

    text = f"Мы уведомили менеджера. Вы можете написать ему напрямую: @{manager_username} \n" \
           f"https://t.me/{manager_username} \n\n Выберите опцию"

    main_menu_markup = create_main_menu_buttons_markup()
    await bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id,
                                reply_markup=main_menu_markup)

