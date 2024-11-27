from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import Router, F

from aiogram_bot.flows.bonuses.keyboards import empty_keyboard
from aiogram_bot.flows.bonuses.state_forms import ClientPhoneForm
from aiogram_bot.flows.bonuses.utils import show_bonus_list, show_bonus, participate_bonus, show_product_feedbacks, \
    register_feedback, register_bonus_request

bonus_router = Router()


# Определяем состояния


@bonus_router.callback_query(F.data == "bonus")
async def instructions_callback(callback: CallbackQuery, state: FSMContext):
    await show_bonus_list(callback, state)


@bonus_router.callback_query(F.data.startswith("bonus_"))
async def view_instruction_callback(callback: CallbackQuery):
    bonus_id = int(callback.data.split("_")[-1])
    await show_bonus(callback, bonus_id)


@bonus_router.callback_query(F.data.startswith("participate_bonus__"))
async def view_instruction_participate_callback(callback: CallbackQuery, state: FSMContext):
    bonus_id = int(callback.data.split("__")[-1])
    await participate_bonus(callback, state, bonus_id)


@bonus_router.callback_query(F.data.startswith("product_feedbacks__"))
async def view_product_feedbacks_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("__")[-1]
    await show_product_feedbacks(callback, state, data)


@bonus_router.callback_query(F.data.startswith("reg_fb__"))
async def view_register_feedback_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("__")[-1]
    await register_feedback(callback, state, data)


@bonus_router.message(ClientPhoneForm.phone)
async def handle_phone(message: Message, state: FSMContext):
    phone = message.text
    if message.contact:
        phone = message.contact.phone_number  # Получаем номер из контакта
        await state.update_data(phone=phone)
        await register_bonus_request(message, state)
        await state.clear()
        # Отправляем сообщение с номером и убираем клавиатуру


    else:
        await message.answer("Пожалуйста, отправьте номер телефона с помощью кнопки.")




