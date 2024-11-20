from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async
from aiogram_bot.flows.instructions.keyboards import instructions_keyboard
from aiogram_bot.flows.main_menu.keyboards import start_keyboard
from aiogram_bot.utils import send_callback_aiogram_message
from apps.instructions.models import Instruction


@sync_to_async
def get_all_instruction_data(instruction_id):
    try:
        instruction = Instruction.objects.get(pk=instruction_id)
        subinstructions = instruction.subinstructions.filter(is_active=True)
        text = f"<b>{instruction.title}</b>\n{instruction.text}"
        photo = None
        if instruction.photo:
            photo_path = instruction.photo.path  # Получаем путь к файлу
            photo = FSInputFile(photo_path)
        print('photo  dd ', photo)
        print('photo  dd ', photo)
        instruction_data = [(text, photo, None)]

        for sub_instr in subinstructions:
            sub_instr_photo = None
            if sub_instr.photo:
                photo_path = sub_instr.photo.path  # Получаем путь к файлу
                sub_instr_photo = FSInputFile(photo_path)

            text, photo = f"<b>{sub_instr.title}</b>\n{sub_instr.text}", sub_instr_photo
            temp = tuple((text, photo, None))
            instruction_data.append(temp)
        return instruction_data
    except:
        return []


async def show_instruction(callback, instruction_id):
    await callback.answer()
    await callback.message.edit_reply_markup()
    instruction_data = await get_all_instruction_data(instruction_id)
    for text, photo, keyboard in instruction_data:
        print('photo ', photo)

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
        text='Выберите инструкцию',
        reply_markup=await instructions_keyboard()
    )


async def show_instruction_list(callback, state):
    await callback.answer()
    await state.clear()

    instructions = await sync_to_async(lambda: list(Instruction.objects.filter(is_active=True)))()
    if len(instructions) == 0:
        await send_callback_aiogram_message(
            callback, 'К сожалению никаких инструкций пока нет. Выберите другие опции:', start_keyboard()
        )
    elif len(instructions) == 1:
        instruction = instructions[0]
        instruction_id = instruction.id
        await show_instruction(callback, instruction_id)

    else:
        await send_callback_aiogram_message(
            callback, 'Выберите инструкцию', await instructions_keyboard()
        )