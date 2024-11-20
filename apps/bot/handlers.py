from telebot.async_telebot import AsyncTeleBot
import logging
from django.conf import settings

from apps.bot.bot import bot
from apps.bot.services.care_service_service import send_care_service_message
from apps.bot.services.instruction_service import show_instruction_list_menu, \
    show_instruction_detail
from apps.bot.services.main_menu_service import send_main_menu, create_start_button
from apps.bot.services.save_user_data_service import save_user_data


# Настроим логирование
logging.basicConfig(level=logging.INFO)

user_last_message = {}


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.send_message(
        message.chat.id,
        "Добро пожаловать!",
        reply_markup=create_start_button()  # Создаем клавиатуру с кнопкой /start
    )
    # Сохраняем данные пользователяx
    user_data = message.from_user
    await save_user_data(user_data)
    await send_main_menu(message)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help'])
async def send_help(message):
    user_data = message.from_user
    user = await save_user_data(user_data)  # асинхронно вызываем функцию для сохранения данных

    # Ответ пользователю
    await bot.send_message(message.chat.id,
                           f"Спасибо, {user.first_name} {user.last_name}!\nВаши данные были сохранены.")


@bot.callback_query_handler(func=lambda call: True)
async def handle_callback_query(call):
    # print(call)
    callback_data = call.data
    if callback_data == "main_menu":
        # Если нажали "Главное меню", возвращаем в главное меню
        await send_main_menu(message=call.message, call=call)
    elif callback_data == "bonus":
        await bot.answer_callback_query(call.id, "Вы выбрали 'Бонус'. Здесь будет информация о бонусах.")
    elif callback_data == "assortment":
        await bot.answer_callback_query(call.id,
                                        "Вы выбрали 'Ассортимент'. Здесь будет информация об ассортименте товаров.")
    elif callback_data == "care_service":
        await send_care_service_message(call)
    elif callback_data == "instructions":
        await show_instruction_list_menu(call=call)

    elif callback_data.startswith("instruction_"):
        # Показать детали инструкции
        await show_instruction_detail(call)


# Обработчик для кнопки "Старт"
@bot.message_handler(func=lambda message: message.text == "Главное меню")
async def handle_start_button(message):
    # Отправляем команду /start в ответ на нажатие кнопки
    await send_welcome(message)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)
