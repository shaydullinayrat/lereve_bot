from telebot.async_telebot import AsyncTeleBot

from core import settings

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='HTML')