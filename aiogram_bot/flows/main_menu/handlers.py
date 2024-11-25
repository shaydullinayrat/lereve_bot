from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command

from aiogram_bot.flows.main_menu import texts
from aiogram_bot.flows.main_menu.keyboards import start_keyboard, main_menu_keyboard
from aiogram_bot.flows.main_menu.utils import save_user_data, get_welcome_text
from aiogram_bot.utils import send_message_aiogram_message, send_callback_aiogram_message

main_menu_router = Router()


# Хендлер команды /start
@main_menu_router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()

    user_data = message.from_user
    await save_user_data(user_data)
    # await message.answer(text='Hello', reply_markup=main_menu_keyboard())

    await send_message_aiogram_message(
        message, get_welcome_text(message), start_keyboard()
    )



@main_menu_router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await send_callback_aiogram_message(
        callback, get_welcome_text(callback.message), start_keyboard()
    )