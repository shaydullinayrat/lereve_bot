from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram_bot.flows.care_service.utils import show_care_service

care_service_router = Router()


@care_service_router.callback_query(F.data == "care_service")
async def care_service_callback(callback: CallbackQuery, state: FSMContext):
    await show_care_service(callback, state)
