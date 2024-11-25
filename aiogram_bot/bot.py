from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.settings import TOKEN_BOT

bot = Bot(token=TOKEN_BOT,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))