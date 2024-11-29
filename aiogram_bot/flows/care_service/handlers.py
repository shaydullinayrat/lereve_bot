from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F, types

from aiogram_bot.flows.care_service.utils import show_care_service, send_message_to_care_service, SupportState, \
    get_client_request, finish_request

care_service_router = Router()


@care_service_router.callback_query(F.data == "care_service")
async def care_service_callback(callback: CallbackQuery, state: FSMContext):
    await show_care_service(callback, state)


@care_service_router.callback_query(F.data.startswith("care_product__"))
async def care_product_callback(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("__")[-1])
    await send_message_to_care_service(callback, state, product_id)


@care_service_router.message(SupportState.describe_issue,
                             F.content_type.in_([types.ContentType.TEXT, types.ContentType.PHOTO,
                                                 types.ContentType.VIDEO, types.ContentType.AUDIO,
                                                 types.ContentType.VOICE]))
async def describe_issue(message: types.Message, state: FSMContext):
    await get_client_request(message, state)


@care_service_router.callback_query(F.data == "finish_request")
async def care_service_finish_request(callback: CallbackQuery, state: FSMContext):
    await finish_request(callback, state)