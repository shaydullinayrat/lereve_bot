from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_bot.flows.main_menu.keyboards import back_to_main_menu_keyboard, start_keyboard
from aiogram_bot.flows.main_menu.texts import back_to_main_menu_text
from aiogram_bot.flows.shops.texts import no_active_shops_text
from aiogram_bot.utils import send_callback_aiogram_message
from apps.shops.models import Shop

def generate_shop_button(shop):
    shop_url = shop.url
    shop_title = shop.title
    text = f'Перейти в магазин {shop_title}'
    row = [InlineKeyboardButton(text=text, url=shop_url)]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[row])
    return keyboard

@sync_to_async
def get_all_shop_data():
    try:
        shops = Shop.objects.all()
        shop_data = []

        for shop in shops:
            shop_photo = None
            if shop.photo:
                photo_path = shop.photo.path  # Получаем путь к файлу
                shop_photo = FSInputFile(photo_path)

            text, photo = f"<b>{shop.title}</b>\n{shop.description}", shop_photo

            keyboard = generate_shop_button(shop)

            temp = tuple((text, photo, keyboard))
            shop_data.append(temp)
        return shop_data
    except:
        return []


async def show_shop_list(callback, state):
    await callback.answer()
    await state.clear()
    await callback.message.edit_reply_markup()



    shops = await sync_to_async(lambda: list(Shop.objects.filter(is_active=True)))()
    if len(shops) == 0:
        await send_callback_aiogram_message(
            callback, no_active_shops_text, start_keyboard()
        )

    else:


        shop_data = await get_all_shop_data()

        for text, photo, keyboard in shop_data:

            if photo is None:
                await callback.message.answer(
                    text=text,
                    reply_markup=keyboard
                )
            else:
                await callback.message.answer_photo(
                    photo=photo,
                    caption=text,
                    reply_markup=keyboard
                )
        await callback.message.answer(
            text=back_to_main_menu_text,
            reply_markup=back_to_main_menu_keyboard()
        )
