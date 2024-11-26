import json

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async

from aiogram_bot.keyboards import generate_linear_keyboard
from apps.bonuses.models import Bonus
from apps.instructions.models import Instruction
from apps.shops.models import Product


@sync_to_async
def bonuses_keyboard():
    # Получаем список активных инструкций из базы данных
    bonuses = Bonus.objects.filter(is_active=True)

    buttons_data = []

    for bonus in bonuses:
        buttons_data.append(
            (bonus.title, f"bonus_{bonus.id}")
        )

    buttons_data.append(
        ('Главное меню', 'start')
    )
    return generate_linear_keyboard(buttons_data)


@sync_to_async
def all_active_products_keyboard():
    # Получаем список активных инструкций из базы данных
    all_active_products = Product.objects.filter(is_active=True, shop__is_active=True)

    buttons_data = []
    # callback_data = callback.new(param1="value1", param2="value2")
    for product in all_active_products:
        text = f'{product.shop.title}: {product.title} - {product.article}'
        buttons_data.append(
            (text, f"bonus_product_{product.id}")
        )

    buttons_data.append(
        ('Назад', 'start')
    )
    return generate_linear_keyboard(buttons_data)


@sync_to_async
def get_all_active_products_keyboard(bonus_id):
    # Получаем список активных инструкций из базы данных
    all_active_products = Product.objects.filter(is_active=True, shop__is_active=True)

    buttons_data = []
    # callback_data = callback.new(param1="value1", param2="value2")
    for product in all_active_products:
        text = f'{product.shop.title}: {product.title} - {product.article}'
        # data = json.dumps({"bonus_id": bonus_id, "article": product.article})

        data = f'bonus_id:{bonus_id}|article:{product.article}'
        buttons_data.append(
            (text, f"product_feedbacks__{data}")
        )
    buttons_data.append(
        ('Назад', 'start')
    )

    return generate_linear_keyboard(buttons_data)


numeric_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3")],
        [KeyboardButton(text="4"), KeyboardButton(text="5"), KeyboardButton(text="6")],
        [KeyboardButton(text="7"), KeyboardButton(text="8"), KeyboardButton(text="9")],
        [KeyboardButton(text="0")],
        [KeyboardButton(text="Отправить номер телефона", request_contact=True)]
    ],
    resize_keyboard=True
)

send_phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Отправить номер телефона 📱", request_contact=True)]
    ],
    resize_keyboard=True
)

# Стандартная клавиатура (или можно оставить пустую)
empty_keyboard = ReplyKeyboardMarkup(
    keyboard=[],  # Пустая клавиатура
    resize_keyboard=True
)
