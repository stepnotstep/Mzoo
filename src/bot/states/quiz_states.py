from aiogram.fsm.state import State, StatesGroup

class QuizSession(StatesGroup):
    question_index = State()