
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


from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Главное меню"),
        # BotCommand(command="bonus", description="Получить бонус"),
        # BotCommand(command="shops", description="Наши магазины"),
        # BotCommand(command="care_service", description="Служба заботы"),
        # BotCommand(command="instructions", description="Как пользоваться"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
