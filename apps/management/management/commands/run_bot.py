from django.core.management.base import BaseCommand, CommandError
import asyncio

from apps.bot.handlers import bot


class Command(BaseCommand):
    help = "Запускаем бота"

    def handle(self, *args, **options):
        asyncio.run(bot.polling())
