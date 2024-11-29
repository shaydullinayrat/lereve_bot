from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async

from aiogram_bot.flows.main_menu.keyboards import start_keyboard
from aiogram_bot.flows.main_menu.texts import welcome_text
from aiogram_bot.utils import get_client_name
from apps.clients.models import Client


async def send_welcome_message(message):
    try:
        await message.edit_text(
            text=get_welcome_text(message),
            reply_markup=start_keyboard()
        )
    except:
        await message.reply_photo(
            photo=get_welcome_photo(),
            caption=get_welcome_text(message),
            reply_markup=start_keyboard()
        )
def get_welcome_text(message):
    client_name = get_client_name(message)
    return welcome_text.format(client_name)

def get_welcome_photo():
    photo = FSInputFile("staticfiles/main_menu_photo.jpeg")
    return photo



@sync_to_async
def save_user_data(user_data):
    user, created = Client.objects.get_or_create(
        user_id=user_data.id,
        defaults={
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'username': user_data.username,
            'language_code': user_data.language_code,
        }
    )

    if not created:
        # Если пользователь уже существует, обновляем информацию
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.username = user_data.username
        user.language_code = user_data.language_code
        user.save()

    return user
