from aiogram import Router
from aiogram.types import Message

from aiogram_bot.flows.main_menu.utils import send_welcome_message

main_router = Router()

@main_router.message()
async def unhandled_message(message: Message):
    if message.text == 'Главное меню':
        await send_welcome_message(message)
        # await send_message_aiogram_message(
        #     message, get_welcome_text(message), start_keyboard()
        # )
    else:
        await send_welcome_message(message)
        # await send_message_aiogram_message(
        #     message, get_welcome_text(message), start_keyboard()
        # )
