from asgiref.sync import sync_to_async

from aiogram_bot.keyboards import generate_linear_keyboard
from apps.shops.models import Product


@sync_to_async
def get_all_active_products_care_keyboard():
    # Получаем список активных инструкций из базы данных
    all_active_products = Product.objects.filter(is_active=True, shop__is_active=True)

    buttons_data = []
    for product in all_active_products:
        text = f'{product.title}'
        buttons_data.append(
            (text, f"care_product__{product.id}")
        )
    buttons_data.append(
        ('Отмена', 'start')
    )


    return generate_linear_keyboard(buttons_data)