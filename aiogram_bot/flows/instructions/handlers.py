from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

from aiogram_bot.flows.instructions.utils import show_instruction_list, show_instruction

instruction_router = Router()

@instruction_router.callback_query(F.data == "instructions")
async def instructions_callback(callback: CallbackQuery, state: FSMContext):
    await show_instruction_list(callback, state)


@instruction_router.callback_query(F.data.startswith("instruction_"))
async def view_instruction_callback(callback: CallbackQuery):
    instruction_id = int(callback.data.split("_")[-1])
    await show_instruction(callback, instruction_id)