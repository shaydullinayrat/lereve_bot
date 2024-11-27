from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram_bot.keyboards import generate_keyboard


def start_keyboard():
    buttons_data = [
        ("Получить бонус", "bonus"),
        ("Наш магазин", "shops"),
        ("Служба заботы", "care_service"),
        ("Как пользоваться", "instructions"),
    ]
    layout = [2, 2]
    return generate_keyboard(buttons_data, layout)


def back_to_main_menu_keyboard():
    buttons_data = [
        ("Главное меню", "start"),
    ]
    layout = [1]
    return generate_keyboard(buttons_data, layout)


def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Главное меню")],
        ],
        resize_keyboard=True
    )
    return keyboard