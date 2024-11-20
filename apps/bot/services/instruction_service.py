import asyncio

from telebot.async_telebot import AsyncTeleBot
from django.conf import settings

from telebot import types
# Главное меню
from apps.bot.bot import bot
from apps.instructions.models import Instruction, SubInstruction


from asgiref.sync import sync_to_async



# Обработчик кнопки "Инструкции"
@sync_to_async
def create_instructions_markup():
    # Получаем список активных инструкций из базы данных
    instructions = Instruction.objects.filter(is_active=True)

    # Создаем inline клавиатуру с кнопками для каждой инструкции
    markup = types.InlineKeyboardMarkup()

    for instruction in instructions:
        # Каждая кнопка будет содержать название инструкции и callback_data с ее ID
        button = types.InlineKeyboardButton(instruction.title, callback_data=f"instruction_{instruction.id}")
        markup.add(button)

    # Добавляем кнопку "Главное меню"
    button_main_menu = types.InlineKeyboardButton("Главное меню", callback_data="main_menu")
    markup.add(button_main_menu)

    return markup


async def show_instruction_list_menu(call):
    await bot.answer_callback_query(call.id)  # Подтверждение клика

    # instructions = await sync_to_async(Instruction.objects.filter(is_active=True))
    instructions = await sync_to_async(lambda: list(Instruction.objects.filter(is_active=True)))()
    if len(instructions) == 1:
        instruction = instructions[0]
        call.data = f'instruction_{instruction.id}'
        await show_instruction_detail(call, back_button='main_menu')
    else:
        instruction_list_markup = await create_instructions_markup()
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=instruction_list_markup)



@sync_to_async
def instruction_detail(instruction_id):
    try:
        instruction = Instruction.objects.get(pk=instruction_id)
        subinstructions = SubInstruction.objects.filter(instruction=instruction, is_active=True).all()
        elements = []
        if instruction.photo:
            elements.append({"type": "photo", "media": instruction.photo})
        elements.append({"type": "text", "content": f"<b>{instruction.title}</b>\n\n{instruction.text}"})

        for sub in subinstructions:
            if sub.photo:
                elements.append({"type": "photo", "media": sub.photo})
            elements.append({"type": "text", "content": f"<b>{sub.title}</b>\n\n{sub.text}"})

        return elements
    except Instruction.DoesNotExist:
        return []


async def show_instruction_detail(call, back_button='back'):
    await bot.answer_callback_query(call.id)
    await bot.delete_message(call.message.chat.id, call.message.id)
    instruction_id = int(call.data.split('_')[1])
    elements = await instruction_detail(instruction_id)
    if elements:
        for element in elements:
            if element["type"] == "photo":
                photo_path = element["media"].path
                with open(photo_path, 'rb') as photo:
                    await bot.send_photo(call.message.chat.id, photo)

            elif element["type"] == "text":
                await bot.send_message(chat_id=call.message.chat.id, text=element["content"], parse_mode='HTML')

        instruction_list_markup = await create_instructions_markup()

        await bot.send_message(chat_id=call.message.chat.id, text="Выберите действие:", reply_markup=instruction_list_markup)