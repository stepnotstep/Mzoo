from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐾 Начать викторину", callback_data="start_quiz")]
    ])

def get_question_keyboard(question_index: int, answers: list):
    buttons = [
        [InlineKeyboardButton(
            text=ans["text"],
            callback_data=f"answer_{question_index}_{i}"
        )]
        for i, ans in enumerate(answers)
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_result_keyboard(animal_key: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Пройти снова", callback_data="start_quiz")],
        [InlineKeyboardButton(text="📢 Поделиться", callback_data=f"share_{animal_key}")],
        [InlineKeyboardButton(text="💬 Отзыв", callback_data="feedback")],
        [InlineKeyboardButton(text="📞 Связаться", callback_data=f"contact_{animal_key}")]
    ])