from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command
from aiogram_bot.flows.care_service.utils import show_care_service

care_service_router = Router()


# @care_service_router.message(Command("care_service"))
# async def care_service_message(message: Message, state: FSMContext):
#     await show_care_service_message(message, state)


@care_service_router.callback_query(F.data == "care_service")
async def care_service_callback(callback: CallbackQuery, state: FSMContext):
    await show_care_service(callback, state)
