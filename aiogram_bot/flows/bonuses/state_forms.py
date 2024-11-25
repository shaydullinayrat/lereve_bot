from aiogram.fsm.state import StatesGroup, State


class BonusRequestForm(StatesGroup):
    bonus = State()
    feedback = State()
    wb_feedback_id = State()
    article = State()
    phone = State()


class ClientPhoneForm(StatesGroup):
    phone = State()
