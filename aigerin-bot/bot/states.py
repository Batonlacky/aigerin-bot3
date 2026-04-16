from aiogram.fsm.state import State, StatesGroup


class Quiz(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    choose_slot = State()
