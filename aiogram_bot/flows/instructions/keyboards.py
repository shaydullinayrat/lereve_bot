from asgiref.sync import sync_to_async

from aiogram_bot.keyboards import generate_linear_keyboard
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
