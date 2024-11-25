from asgiref.sync import sync_to_async

from aiogram_bot.keyboards import generate_linear_keyboard, generate_keyboard
from apps.instructions.models import Instruction

@sync_to_async
def instructions_keyboard():
    # Получаем список активных инструкций из базы данных
    instructions = Instruction.objects.filter(is_active=True)

    buttons_data = []

    for instruction in instructions:
        buttons_data.append(
            (instruction.title, f"instruction_{instruction.id}")
        )

    buttons_data.append(
        ('Главное меню', 'start')
    )
    return generate_linear_keyboard(buttons_data)

async def subinstruction_keyboard(next_subinstruction_id, back_button='instructions'):
    if next_subinstruction_id:
        buttons_data = [
            ("Назад", back_button),
            ("Дальше", f"subinstruction_{next_subinstruction_id}"),

        ]
        layout = [2]
        return generate_keyboard(buttons_data, layout)
    else:
        return await instructions_keyboard()

