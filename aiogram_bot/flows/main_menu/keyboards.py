from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram_bot.keyboards import generate_keyboard


def start_keyboard_old():
    buttons_data = [
        ("Получить бонус", "bonus"),
        ("Наш магазин", "shops"),
        ("Служба заботы", "care_service"),
        ("Как пользоваться", "instructions"),
    ]
    layout = [2, 2]
    return generate_keyboard(buttons_data, layout)


def start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Получить бонус", callback_data="bonus"),
                InlineKeyboardButton(text="Как пользоваться", callback_data="instructions"),

            ],
            [
                InlineKeyboardButton(text="Служба заботы", url="https://t.me/rishat_1988"),
                InlineKeyboardButton(text="Наш магазин", url="https://www.wildberries.ru/brands/le-reve/duhi"),
            ],
        ]
    )
    return keyboard



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