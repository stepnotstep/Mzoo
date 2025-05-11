import random
import logging
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.bot.handlers.result import ANIMALS_DATA, show_result_with_animal

router = Router()
logger = logging.getLogger("zoo_bot.handlers.test")

@router.message(lambda message: message.text.startswith("/test_result"))
async def test_result(message: types.Message, state: FSMContext):
    """
    Тестовая команда для вывода результата без прохождения викторины.
    Использование:
      /test_result         -> случайное животное
      /test_result ёж     -> показать ёжа
    """
    logger.info(f"Пользователь {message.from_user.id} вызвал /test_result")

    # Определяем животное
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    animal_key = args[0] if args and args[0] in ANIMALS_DATA else None

    if not animal_key:
        animal_key = random.choice(list(ANIMALS_DATA.keys()))
        logger.debug(f"Выбрано случайное животное: {animal_key}")

    if animal_key not in ANIMALS_DATA:
        await message.answer(
            f"⚠️ Животное '{animal_key}' не найдено. Попробуйте:\n"
            f"{', '.join(ANIMALS_DATA.keys())}"
        )
        return

    # Передаем животное в функцию отображения результата
    await show_result_with_animal(message, state, animal_key)