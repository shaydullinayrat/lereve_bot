from django.core.management.base import BaseCommand
from aiogram_bot.main import start_bot
import asyncio

class Command(BaseCommand):
    help = "Запуск Telegram-бота"

    def handle(self, *args, **kwargs):
        self.stdout.write("Запускаем Telegram-бота...")
        asyncio.run(start_bot())
