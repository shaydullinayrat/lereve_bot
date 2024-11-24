import json

from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async

from aiogram_bot import main
from aiogram_bot.flows.bonuses.keyboards import bonuses_keyboard
from aiogram_bot.flows.bonuses.texts import no_active_bonus_text
from aiogram_bot.flows.bonuses.wb_service import get_recent_comments, TEST_NMID
from aiogram_bot.flows.main_menu.keyboards import start_keyboard, back_to_main_menu_keyboard
from aiogram_bot.keyboards import generate_keyboard
from aiogram_bot.tasks import redis_client
from aiogram_bot.utils import send_callback_aiogram_message
from apps.bonuses.models import Bonus
from core.settings import TELEGRAM_MANAGER_ID, TELEGRAM_MANAGER_USERNAME


@sync_to_async
def get_bonus_data(bonus_id):
    try:
        bonus = Bonus.objects.get(pk=bonus_id)
        text = f"<b>{bonus.title}</b>\n{bonus.description}"
        photo = None
        if bonus.photo:
            photo_path = bonus.photo.path  # Получаем путь к файлу
            photo = FSInputFile(photo_path)
        bonus_data = (text, photo, None)

        return bonus_data
    except:
        return None


async def show_bonus_list(callback, state):
    await callback.answer()
    await state.clear()

    # await get_recent_comments(TEST_NMID)
    # fetch_feedbacks()

    from django.core.cache import cache

    # Извлекаем данные

    feedbacks = json.loads(redis_client.get('feedbacks'))
    if feedbacks:
        print('feedbacks')
        print(feedbacks)
    else:
        print('Нет данных для этого ключа.')

    bonuses = await sync_to_async(lambda: list(Bonus.objects.filter(is_active=True)))()
    if len(bonuses) == 0:
        await send_callback_aiogram_message(
            callback, no_active_bonus_text, start_keyboard()
        )
    elif len(bonuses) == 1:
        bonus = bonuses[0]
        bonus_id = bonus.id
        await show_bonus(callback, bonus_id, back_button='start')

    else:
        await send_callback_aiogram_message(
            callback, 'Выберите бонус', await bonuses_keyboard()
        )


async def show_bonus(callback, bonus_id, back_button='bonus'):
    await callback.answer()
    await callback.message.edit_reply_markup()
    try:
        bonus = await Bonus.objects.aget(pk=bonus_id)
        if bonus:
            bonus_text = f'<b>{bonus.title}</b> \n {bonus.description}'

            buttons_data = [
                ("Назад", back_button),
                ("Участвую!", f"participate_bonus_{bonus_id}"),
            ]
            layout = [2]
            keyboard = generate_keyboard(buttons_data, layout)
            if bonus.photo:
                photo_path = bonus.photo.path  # Получаем путь к файлу
                photo = FSInputFile(photo_path)
                await callback.message.answer_photo(
                    photo=photo,
                    caption=bonus_text,
                    reply_markup=keyboard
                )
            else:
                await callback.message.answer(
                    text=bonus_text,
                    reply_markup=keyboard
                )

    except:
        callback.message.answer(
            text='К сожалению нет активных бонусов',
            reply_markup=back_to_main_menu_keyboard()
        )


async def participate_bonus(callback, bonus_id):
    await callback.answer()
    await callback.message.edit_reply_markup()
    try:
        bonus = await Bonus.objects.aget(pk=bonus_id)
        manager_chat_id = TELEGRAM_MANAGER_ID  # Укажите реальный chat_id менеджера
        manager_username = TELEGRAM_MANAGER_USERNAME  # Укажите реальный chat_id менеджера
        user_info = f"Пользователь: @{callback.from_user.username} (ID: {callback.from_user.id})"

        await main.bot.send_message(manager_chat_id,
                                    f"{user_info} хочет учавствовать в бонусной программе: {bonus.title}")
        manager_contact_text = f"Напишите администратору все необходимые данные: @{manager_username}"

        await callback.message.answer(
            text=manager_contact_text,
            reply_markup=back_to_main_menu_keyboard()
        )
    except:
        callback.message.answer(
            text='К сожалению нет активных бонусов',
            reply_markup=back_to_main_menu_keyboard()
        )


