from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command
from aiogram_bot.flows.instructions.utils import show_instruction_list, show_instruction, show_subinstruction

instruction_router = Router()

# @instruction_router.message(Command("instructions"))
# async def instructions_message(message: Message, state: FSMContext):
#     await show_instruction_list_message(message, state)
@instruction_router.callback_query(F.data == "instructions")
async def instructions_callback(callback: CallbackQuery, state: FSMContext):
    await show_instruction_list(callback, state)


@instruction_router.callback_query(F.data.startswith("instruction_"))
async def view_instruction_callback(callback: CallbackQuery):
    instruction_id = int(callback.data.split("_")[-1])
    await show_instruction(callback, instruction_id)


@instruction_router.callback_query(F.data.startswith("subinstruction_"))
async def view_instruction_callback(callback: CallbackQuery):
    subinstruction_id = int(callback.data.split("_")[-1])
    await show_subinstruction(callback, subinstruction_id)