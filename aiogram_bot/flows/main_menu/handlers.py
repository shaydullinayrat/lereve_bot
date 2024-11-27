from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command

from aiogram_bot.flows.main_menu.utils import save_user_data, send_welcome_message

main_menu_router = Router()


# Хендлер команды /start
@main_menu_router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()

    user_data = message.from_user
    await save_user_data(user_data)

    # Отправка сообщения с фото через message
    await send_welcome_message(message)


@main_menu_router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await send_welcome_message(callback.message)
