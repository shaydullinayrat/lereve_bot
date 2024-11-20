
from aiogram.types import Message


async def send_callback_aiogram_message(callback, text, keyboard=None):
    try:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    except:
        await callback.message.edit_reply_markup()
        await callback.message.answer(text=text, reply_markup=keyboard)


async def send_message_aiogram_message(message: Message, text, keyboard=None):
    try:
        await message.edit_text(text=text, reply_markup=keyboard)
    except:
        await message.answer(text=text, reply_markup=keyboard)
