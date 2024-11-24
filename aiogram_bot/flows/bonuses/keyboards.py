from asgiref.sync import sync_to_async

from aiogram_bot.keyboards import generate_linear_keyboard
from apps.bonuses.models import Bonus
from apps.instructions.models import Instruction

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
