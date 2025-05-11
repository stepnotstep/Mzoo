import os
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()
logger = logging.getLogger("zoo_bot.handlers.feedback")

# 1) Определяем состояние для ввода отзыва
class FeedbackState(StatesGroup):
    waiting_for_feedback = State()

# 2) Хэндлер кнопки “💬 Отзыв”
@router.callback_query(F.data == "feedback")
async def start_user_feedback(callback: CallbackQuery, state: FSMContext):
    """
    Запускает сбор отзыва от пользователя.
    Переводит бота в состояние ожидания текстового сообщения.
    """
    user = callback.from_user
    logger.info(f"Пользователь {user.id} начал оставлять отзыв")
    
    await callback.message.answer(
        "💌 Поделитесь своими впечатлениями — что вам понравилось или что можно улучшить:"
    )
    await state.set_state(FeedbackState.waiting_for_feedback)
    await callback.answer()

# 3) Хэндлер получения текста отзыва
@router.message(FeedbackState.waiting_for_feedback)
async def receive_user_feedback(message: Message, state: FSMContext):
    """
    Обрабатывает введённый пользователем отзыв:
    — сохраняет его в файл,
    — отправляет подтверждение,
    — завершает состояние.
    """
    user = message.from_user
    feedback_text = message.text.strip()
    username = user.username or user.first_name

    # Путь к файлу с отзывами
    feedback_dir = 'data'
    os.makedirs(feedback_dir, exist_ok=True)
    feedback_path = os.path.join(feedback_dir, 'feedbacks.txt')

    # Сохраняем отзыв в файл
    try:
        with open(feedback_path, 'a', encoding='utf-8') as f:
            f.write(f"{user.id} (@{username}): {feedback_text}\n")
        logger.info(f"Отзыв от пользователя {user.id} успешно сохранён")
        await message.answer("Спасибо за ваше мнение! ❤️")
    except Exception as e:
        logger.exception(f"Ошибка при сохранении отзыва от {user.id}: {e}")
        await message.answer("⚠️ Не удалось сохранить отзыв. Попробуйте позже.")

    # Сброс состояния
    await state.clear()