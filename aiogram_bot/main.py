from aiogram import Bot, Dispatcher
import logging

# Инициализация бота
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram_bot.flows.bonuses.handlers import bonus_router
from aiogram_bot.flows.care_service.handlers import care_service_router
from aiogram_bot.flows.instructions.handlers import instruction_router
from aiogram_bot.flows.main_menu.handlers import main_menu_router
from aiogram_bot.flows.shops.handlers import shops_router
from aiogram_bot.handlers import main_router
from aiogram_bot.utils import set_default_commands
from core.settings import TOKEN_BOT

bot = Bot(token=TOKEN_BOT,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()



# Регистрация роутеров
# dp.include_router(user_router)
dp.include_router(main_menu_router)
dp.include_router(instruction_router)
dp.include_router(care_service_router)
dp.include_router(shops_router)
dp.include_router(bonus_router)


dp.include_router(main_router)
# Логирование
logging.basicConfig(level=logging.INFO)


# Функция запуска бота
async def start_bot():
    # Установка команд
    await set_default_commands(bot)
    await dp.start_polling(bot)
