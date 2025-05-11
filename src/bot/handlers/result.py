import os
import logging
from typing import Optional, Dict, Any
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, User
from aiogram.fsm.context import FSMContext

from src.bot.core.config import GUARDIAN_LINK
from src.bot.services.media import generate_result_image
from src.bot.services.scoring import calculate_scores, determine_top_animal
from src.bot.keyboards.buttons import get_result_keyboard
from src.bot.services.data_loader import load_animals


def get_user_display_name(user: User) -> str:
    """
    Возвращает отображаемое имя пользователя.
    Приоритет: full_name → username → 'Друг'.
    """
    if user.full_name:
        return user.full_name
    elif user.username:
        return user.username
    else:
        return "Друг"

router = Router()
logger = logging.getLogger("zoo_bot.handlers.result")

# Загружаем информацию о животных
ANIMALS_DATA = load_animals()

async def show_result(message: Message, state: FSMContext):
    """
    Отображает результат викторины:
    1) Получает собранные ответы из состояния,
    2) Рассчитывает тотемное животное,
    3) Генерирует изображение с результатом,
    4) Отправляет пользователю сообщение и картинку,
    5) Сбрасывает состояние.
    """
    data = await state.get_data()
    answers = data.get("selected_answers", [])

    # 1) Подсчёт очков за ответы
    scores = calculate_scores(answers)
    top_animal = determine_top_animal(scores)

    if not top_animal:
        logger.warning(f"Нет данных для определения тотемного животного у пользователя {message.from_user.id}")
        await message.answer("⚠️ Не удалось определить ваше тотемное животное. Попробуйте ещё раз.")
        await state.clear()
        return

    animal_key, score = top_animal
    animal_info = ANIMALS_DATA.get(animal_key)

    if not animal_info:
        logger.error(f"Животное '{animal_key}' не найдено в базе данных")
        await message.answer("⚠️ Произошла ошибка при определении тотема.")
        await state.clear()
        return

    logger.info(f"Пользователь {message.from_user.id} — тотем: {animal_info['name']} ({score} баллов)")

    # 2) Генерация изображения
    image_path = None
    try:
        image_path = await generate_result_image(
            animal_image=animal_info["image"],
            animal_name=animal_info["name"],
            user_name=get_user_display_name(message.from_user)
        )
    except Exception as e:
        logger.exception(f"Ошибка при генерации изображения для {animal_key}: {e}")

    # 3) Формирование текста результата
    caption = (
        f"_{animal_info['description']}_\n\n"

        "🐾  Ты прошёл викторину и узнал своё тотемное животное. "
        "А теперь представь, что ты можешь стать ему настоящей поддержкой.\n\n"

        "🌿 В Московском зоопарке каждый может взять под опеку не просто какое-то животное, "
        "а того, кто ближе по духу. Того, чья история тебя тронула. Того, кем ты восхищаешься.\n\n"

        "Ты можешь:\n"
        "• стать опекуном *именно своего тотемного* животного,\n"
        "• выбрать любого другого из 1100 видов,\n"
        "• подарить опеку или сделать пожертвование от лица компании.\n\n"

        "🫶 Это шанс быть частью чего-то большего.\n"
        "Помогать ежедневно, даже без больших затрат.\n\n"

        f"[💚 Подробнее о программе опеки]({GUARDIAN_LINK})"
    )

    # 4) Создание клавиатуры
    keyboard = get_result_keyboard(animal_key)

    # 5) Отправка результата (картинка или текст)
    try:
        if image_path:
            from aiogram.types import FSInputFile
            photo = FSInputFile(image_path)
            await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard, parse_mode="Markdown")
        else:
            await message.answer(text=caption, reply_markup=keyboard, parse_mode="Markdown")
    except Exception as e:
        logger.exception(f"Ошибка при отправке результата пользователю {message.from_user.id}: {e}")
        await message.answer("⚠️ Не удалось отправить результат. Попробуйте позже.")

    # 6) Сброс состояния
    await state.clear()


# тестовая функция для вывода результата без прохождения викторины
async def show_result_with_animal(message: Message, state: FSMContext, animal_key: str):
    """
    Показывает результат викторины для заданного animal_key.
    Используется для тестирования (/test_result).
    """
    animal = ANIMALS_DATA.get(animal_key)

    if not animal:
        logger.error(f"Totem key '{animal_key}' отсутствует в animals.json")
        await message.answer("⚠️ Не удалось определить тотемное животное.")
        return

    logger.info(f"Тестовый режим: пользователь {message.from_user.id} получил животное '{animal['name']}'")

    # Генерация картинки
    try:
        image_path = await generate_result_image(
            animal_image=animal["image"],
            animal_name=animal["name"],
            user_name=get_user_display_name(message.from_user)
        )
    except Exception as e:
        logger.exception(f"Ошибка генерации изображения для тестового результата: {e}")
        image_path = None

    # Формирование текста
    # caption = (
    #     f"🎉 *Твоё тотемное животное — {animal['name']}!*\n"
    #     f"_{animal['description']}_\n\n"
    #     f"[Узнать об опеке]({animal['guardian_link']})"
    # )
    caption = (
        f"_{animal['description']}_\n\n"

        "🐾  Ты прошёл викторину и узнал своё тотемное животное. "
        "А теперь представь, что ты можешь стать ему настоящей поддержкой.\n\n"

        "🌿 В Московском зоопарке каждый может взять под опеку не просто какое-то животное, "
        "а того, кто ближе по духу. Того, чья история тебя тронула. Того, кем ты восхищаешься.\n\n"

        "Ты можешь:\n"
        "• стать опекуном *именно своего тотемного* животного,\n"
        "• выбрать любого другого из 1100 видов,\n"
        "• подарить опеку или сделать пожертвование от лица компании.\n\n"

        "🫶 Это шанс быть частью чего-то большего.\n"
        "Помогать ежедневно, даже без больших затрат.\n\n"

        f"[💚 Подробнее о программе опеки]({GUARDIAN_LINK})"
    )

    # Кнопки
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Пройти снова", callback_data="start_quiz")],
        [InlineKeyboardButton(text="📢 Поделиться", callback_data=f"share_{animal_key}")],
        [InlineKeyboardButton(text="💬 Отзыв", callback_data="feedback")],
        [InlineKeyboardButton(text="📞 Связаться", callback_data=f"contact_{animal_key}")]
    ])

    # Отправка результата
    if image_path:
        from aiogram.types import FSInputFile
        photo = FSInputFile(image_path)
        await message.answer_photo(photo=photo, caption=caption, parse_mode="Markdown", reply_markup=kb)
    else:
        await message.answer(caption, parse_mode="Markdown", reply_markup=kb)

    # Сбрасываем состояние (если оно было)
    await state.clear()