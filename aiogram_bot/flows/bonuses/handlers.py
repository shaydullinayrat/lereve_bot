from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

from aiogram_bot.flows.bonuses.utils import show_bonus_list, show_bonus, participate_bonus

bonus_router = Router()

@bonus_router.callback_query(F.data == "bonus")
async def instructions_callback(callback: CallbackQuery, state: FSMContext):
    await show_bonus_list(callback, state)

@bonus_router.callback_query(F.data.startswith("bonus_"))
async def view_instruction_callback(callback: CallbackQuery):
    bonus_id = int(callback.data.split("_")[-1])
    await show_bonus(callback, bonus_id)

@bonus_router.callback_query(F.data.startswith("participate_bonus_"))
async def view_instruction_participate_callback(callback: CallbackQuery):
    bonus_id = int(callback.data.split("_")[-1])
    await participate_bonus(callback, bonus_id)