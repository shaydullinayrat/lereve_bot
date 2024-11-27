from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async
from aiogram_bot.flows.main_menu.keyboards import start_keyboard
from aiogram_bot.flows.shops.keyboards import generate_shop_button
from aiogram_bot.flows.shops.texts import no_active_shops_text
from aiogram_bot.utils import send_callback_aiogram_message
from apps.shops.models import Shop


@sync_to_async
def get_all_shop_data():
    try:
        shops = Shop.objects.filter(is_active=True)
        shops_count = shops.count()
        shop_data = []
        is_last = False
        k = 0
        for shop in shops:
            k += 1
            shop_photo = None
            if shop.photo:
                photo_path = shop.photo.path  # Получаем путь к файлу
                shop_photo = FSInputFile(photo_path)

            text, photo = f"<b>{shop.title}</b>\n\n{shop.description}", shop_photo
            if k == shops_count:
                is_last = True

            keyboard = generate_shop_button(shop, is_last)

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
        # await callback.message.answer(
        #     text=back_to_main_menu_text,
        #     reply_markup=back_to_main_menu_keyboard()
        # )
