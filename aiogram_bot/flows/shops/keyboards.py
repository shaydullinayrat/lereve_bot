from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram_bot.flows.shops.texts import go_to_shop


def generate_shop_button(shop, is_last=False):
    shop_url = shop.url
    shop_title = shop.title
    text = f'{go_to_shop} {shop_title}'
    row = [InlineKeyboardButton(text=text, url=shop_url)]
    main_menu_button = [InlineKeyboardButton(text='Главное меню', callback_data='start')]
    if is_last:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[row, main_menu_button])
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[row])
    return keyboard