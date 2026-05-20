from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    choosing_class = State()