# src/bot/handlers/start.py
import logging
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

router = Router()
logger = logging.getLogger("zoo_bot.handlers.start")

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Отправляет приветственное сообщение с изображением логотипа
    и приглашает пользователя пройти викторину.
    """
    user = message.from_user
    logger.info(f"Пользователь {user.id} начал взаимодействие")

    # Путь к логотипу
    logo_path = "media/logo/mzoo_logo_post.png"
    post_text = (
            "🐺 Добро пожаловать в квиз «Тотемное животное»!\n\n"
            "✋😃 Привет! Я — бот от Московского зоопарка. Здесь ты пройдёшь короткую викторину и узнаешь, "
            "какое животное больше всего похоже на тебя.\n\n"
            "**Как играть:**\n"
            "1. Нажми кнопку «Начать викторину»\n"
            "2. Отвечай на вопросы, нажимая на варианты ответов\n"
            "3. Узнай своё тотемное животное, поделись результатом с друзьями!\n\n"
            "🤗 А может, ты захочешь ухаживать за своим тотемных животным в Московском зоопарке?!\n\n"
            "А пока начнём с малого — узнай себя в мире животных 🐾"
        )
    
    try:
        photo = FSInputFile(logo_path)
        caption = post_text

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🐾 Начать викторину", callback_data="start_quiz")]
        ])

        await message.answer_photo(
            photo=photo,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Не удалось отправить фото: {e}")
        # Если не получилось отправить с фото — просто текст
        fallback_text = post_text
        await message.answer(
            text=fallback_text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )