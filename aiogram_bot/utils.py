
from aiogram.types import Message


def get_client_name(message):
    first_name = message.from_user.first_name
    client_name = 'Дорогой клиент'
    if first_name and 'Ле Реве' not in first_name and 'Le Reve' not in first_name:
        client_name = f'{first_name}'
    return client_name


async def send_callback_aiogram_message(callback, text, keyboard=None, disable_web_page_preview=False):
    try:
        await callback.message.edit_text(text=text, reply_markup=keyboard, disable_web_page_preview=disable_web_page_preview)
    except:
        await callback.message.edit_reply_markup()
        await callback.message.answer(text=text, reply_markup=keyboard, disable_web_page_preview=disable_web_page_preview)


async def send_message_aiogram_message(message: Message, text, keyboard=None, disable_web_page_preview=False):
    try:
        await message.edit_text(text=text, reply_markup=keyboard, disable_web_page_preview=disable_web_page_preview)
    except:
        await message.answer(text=text, reply_markup=keyboard, disable_web_page_preview=disable_web_page_preview)


from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Главное меню"),
        # BotCommand(command="bonus", description="Получить бонус"),
        # BotCommand(command="shops", description="
        # Наши магазины"),
        # BotCommand(command="care_service", description="Служба заботы"),
        # BotCommand(command="instructions", description="Как пользоваться"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


from datetime import datetime
import locale


def format_date_iso_to_russian(date_str):
    """
    Преобразует дату из форматов ISO 8601 с таймзоной (Z или +03:00) в формат: "26 сентября 2024, 10:20:48".

    :param date_str: Строка даты в формате ISO 8601, например, "2024-09-26T10:20:48+03:00" или "2024-09-26T10:20:48Z".
    :return: Отформатированная строка на русском языке.
    """
    try:
        # Устанавливаем локаль для отображения месяца на русском языке
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        # Парсим строку в объект datetime
        if date_str.endswith("Z"):  # Обработка UTC формата с "Z"
            parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        else:  # Обработка формата с таймзоной "+03:00"
            parsed_date = datetime.fromisoformat(date_str)

        # Форматируем дату в нужном виде
        formatted_date = parsed_date.strftime("%d %B %Y, %H:%M:%S")

        # Делаем первую букву месяца строчной
        formatted_date = formatted_date.replace(formatted_date.split()[1], formatted_date.split()[1].lower(), 1)

        return formatted_date
    except Exception as e:
        return f"Ошибка: {e}"






