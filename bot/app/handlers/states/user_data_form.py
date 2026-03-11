from aiogram.fsm.state import State, StatesGroup


class UserDataForm(StatesGroup):
    """FSM для формы запроса контактных данных"""
    waiting_for_phone = State()
    waiting_for_location = State()
