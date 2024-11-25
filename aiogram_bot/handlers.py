from aiogram import Router
from aiogram.types import Message

from aiogram_bot.flows.main_menu.keyboards import start_keyboard
from aiogram_bot.flows.main_menu.texts import welcome_text
from aiogram_bot.flows.main_menu.utils import get_welcome_text
from aiogram_bot.utils import send_message_aiogram_message

main_router = Router()

@main_router.message()
async def unhandled_message(message: Message):
    if message.text == 'Главное меню':
        await send_message_aiogram_message(
            message, get_welcome_text(message), start_keyboard()
        )
    else:
        await send_message_aiogram_message(
            message, get_welcome_text(message), start_keyboard()
        )
        # await message.answer(f"Не знаю, что с этим делать: {message.text}")
