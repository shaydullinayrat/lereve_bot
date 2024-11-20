from aiogram_bot.keyboards import generate_keyboard


def start_keyboard():
    buttons_data = [
        ("Получить бонус", "bonus"),
        ("Наш ассортимент", "assortment"),
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