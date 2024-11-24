from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

from aiogram_bot.flows.shops.utils import show_shop_list

shops_router = Router()

from aiogram.filters import Command



# @shops_router.message(Command("shops"))
# async def instructions_message(message: Message, state: FSMContext):
#     print('asdasd')
#     await show_shop_list_message(message, state)
@shops_router.callback_query(F.data == "shops")
async def instructions_callback(callback: CallbackQuery, state: FSMContext):
    await show_shop_list(callback, state)