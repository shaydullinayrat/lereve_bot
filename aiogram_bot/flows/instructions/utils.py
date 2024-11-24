from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async
from aiogram_bot.flows.instructions.keyboards import instructions_keyboard, subinstruction_keyboard
from aiogram_bot.flows.instructions.texts import no_active_instructions_text
from aiogram_bot.flows.main_menu.keyboards import start_keyboard
from aiogram_bot.flows.main_menu.texts import welcome_text
from aiogram_bot.utils import send_callback_aiogram_message, send_message_aiogram_message
from apps.instructions.models import Instruction, SubInstruction


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


async def show_instruction2(callback, instruction_id):
    await callback.answer()
    await callback.message.edit_reply_markup()
    instruction_data = await get_all_instruction_data(instruction_id)
    for text, photo, keyboard in instruction_data:

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
            callback, no_active_instructions_text, start_keyboard()
        )
    elif len(instructions) == 1:
        instruction = instructions[0]
        instruction_id = instruction.id
        await show_instruction(callback, instruction_id)

    else:
        await send_callback_aiogram_message(
            callback, 'Выберите инструкцию', await instructions_keyboard()
        )


@sync_to_async
def get_first_subinstruction(instruction):
    next_subinstructions = instruction.subinstructions.order_by('order')
    next_subinstruction = next_subinstructions.first()
    if next_subinstruction:
        return next_subinstruction.id
    return None


@sync_to_async
def get_next_subinstruction_from_subinstruction(subinstruction):
    instruction = subinstruction.instruction
    next_subinstructions = instruction.subinstructions.order_by('order').filter(order__gt=subinstruction.order)
    next_subinstruction = next_subinstructions.first()
    if next_subinstruction:
        return next_subinstruction.id
    return None


async def show_subinstruction(callback, subinstruction_id):
    subinstruction = await SubInstruction.objects.aget(pk=subinstruction_id)
    if subinstruction:
        next_subinstruction_id = await get_next_subinstruction_from_subinstruction(subinstruction)
        keyboard = await subinstruction_keyboard(next_subinstruction_id)

        text = f'<b>{subinstruction.title}</b>\n{subinstruction.text}'

        if subinstruction.photo:
            photo_path = subinstruction.photo.path  # Получаем путь к файлу
            photo = FSInputFile(photo_path)
            await callback.message.answer_photo(
                photo=photo,
                caption=text,
                reply_markup=keyboard
            )
        else:
            await callback.message.answer(
                text=text,
                reply_markup=keyboard
            )
    else:
        await send_message_aiogram_message(
            callback.message, welcome_text, start_keyboard()
        )


async def show_instruction(callback, instruction_id):
    instruction = await Instruction.objects.prefetch_related("subinstructions").aget(pk=instruction_id)
    if instruction:
        next_subinstruction_id = await get_first_subinstruction(instruction)

        keyboard = await subinstruction_keyboard(next_subinstruction_id)

        text = f'<b>{instruction.title}</b>\n{instruction.text}'

        if instruction.photo:
            photo_path = instruction.photo.path  # Получаем путь к файлу
            photo = FSInputFile(photo_path)
            await callback.message.answer_photo(
                photo=photo,
                caption=text,
                reply_markup=keyboard
            )
        else:
            await callback.message.answer(
                text=text,
                reply_markup=keyboard
            )
    else:
        await send_message_aiogram_message(
            callback.message, welcome_text, start_keyboard()
        )
