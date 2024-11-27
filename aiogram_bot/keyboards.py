from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_linear_keyboard(buttons_data):
    buttons = []
    for button in buttons_data:
        row = [
            InlineKeyboardButton(
                text=button[0], callback_data=button[1]
            )
        ]
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def generate_keyboard(buttons_data, layout):
    buttons = []
    index = 0

    for row_size in layout:
        row = [
            InlineKeyboardButton(
                text=buttons_data[i][0], callback_data=buttons_data[i][1]
            )
            for i in range(index, index + row_size)
        ]
        buttons.append(row)
        index += row_size

    return InlineKeyboardMarkup(inline_keyboard=buttons)

