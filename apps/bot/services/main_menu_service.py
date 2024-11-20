from telebot.async_telebot import AsyncTeleBot
from django.conf import settings
from telebot import types

from apps.bot.bot import bot


def create_start_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Главное меню")  # Кнопка /start
    )
    return markup

def create_main_menu_buttons_markup():
    # Создаем inline клавиатуру
    markup = types.InlineKeyboardMarkup()
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Создаем кнопки
    bonus_button = types.InlineKeyboardButton("Бонус", callback_data="bonus")
    assortment_button = types.InlineKeyboardButton("Ассортимент", callback_data="assortment")
    care_service_button = types.InlineKeyboardButton("Служба заботы", callback_data="care_service")
    # care_service_button = types.InlineKeyboardButton("Служба заботы", url=f'https://t.me/shaydullinayrat')
    # care_service_button2 = types.InlineKeyboardButton("Служба заботы 2 ", callback_data="care_service")
    instructions_button = types.InlineKeyboardButton("Как пользоваться", callback_data="instructions")

    # Добавляем кнопки в клавиатуру
    markup.add(bonus_button, assortment_button)
    markup.add(care_service_button, instructions_button)

    return markup



async def send_main_menu(message, call=None):
    main_menu_markup = create_main_menu_buttons_markup()

    if call:
        await bot.answer_callback_query(call.id)  # Подтверждение клика
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id,
                                            reply_markup=main_menu_markup)
    else:
        await bot.send_message(
            message.chat.id,
            "Выберите одну из опций:",
            reply_markup=main_menu_markup
        )

