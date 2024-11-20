from aiogram import Router
from aiogram.types import Message

main_router = Router()

@main_router.message()
async def unhandled_message(message: Message):
    await message.answer(f"Не знаю, что с этим делать: {message.text}")