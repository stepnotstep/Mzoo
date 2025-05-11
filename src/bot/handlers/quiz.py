import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from src.bot.states.quiz_states import QuizSession
from src.bot.services.data_loader import load_questions
from src.bot.keyboards.buttons import get_question_keyboard

router = Router()
logger = logging.getLogger("zoo_bot.handlers.quiz")

# Загружаем вопросы из JSON-файла
QUESTIONS = load_questions()
TOTAL_QUESTIONS = len(QUESTIONS)

logger.info(f"Загружено {TOTAL_QUESTIONS} вопросов для викторины")


@router.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки «🐾 Начать викторину».
    Очищает предыдущее состояние и начинает новую сессию.
    """
    await state.clear()
    await state.update_data(current_index=0, selected_answers=[])
    logger.info(f"Пользователь {callback.from_user.id} начал викторину")
    await ask_question(callback.message, 0, state)
    await callback.answer()


async def ask_question(message: Message, index: int, state: FSMContext):
    """
    Отправляет пользователю очередной вопрос по индексу.
    Если вопросы закончились — переходим к результатам.
    """
    if index >= TOTAL_QUESTIONS:
        logger.info(f"Все вопросы пройдены для пользователя {message.from_user.id}")
        from src.bot.handlers.result import show_result
        await show_result(message, state)
        return

    question = QUESTIONS[index]
    keyboard = get_question_keyboard(index, question["answers"])

    await message.answer(
        f"❓ Вопрос {index + 1}/{TOTAL_QUESTIONS}:\n"
        f"{question['question']}",
        reply_markup=keyboard
    )
    await state.set_state(QuizSession.question_index)


@router.callback_query(F.data.startswith("answer_"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор ответа пользователем.
    Сохраняет выбранные веса и переходит к следующему вопросу.
    """
    data = await state.get_data()
    current_index = data.get("current_index", 0)
    selected_answers = data.get("selected_answers", [])

    # Извлекаем индексы вопроса и ответа из callback_data
    _, q_idx_str, a_idx_str = callback.data.split("_")
    q_idx, a_idx = int(q_idx_str), int(a_idx_str)

    # Получаем веса выбранного ответа
    answer_weights = QUESTIONS[q_idx]["answers"][a_idx]["weights"]
    selected_answers.append(answer_weights)

    await state.update_data(current_index=current_index + 1, selected_answers=selected_answers)

    # Убираем клавиатуру у текущего сообщения
    await callback.message.edit_reply_markup(reply_markup=None)
    logger.debug(f"Пользователь {callback.from_user.id} выбрал ответ {a_idx} на вопрос {q_idx}")

    # Переходим к следующему вопросу
    await ask_question(callback.message, current_index + 1, state)
    await callback.answer()