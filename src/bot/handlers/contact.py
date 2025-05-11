import os
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()
logger = logging.getLogger("zoo_bot.handlers.contact")

@router.callback_query(F.data.startswith("contact_"))
async def handle_contact_request(callback: CallbackQuery):
    """
    Обрабатывает нажатие кнопки "📞 Связаться":
    — собирает информацию о пользователе и его тотемном животном,
    — сохраняет запрос в файл,
    — отправляет подтверждение пользователю.
    """
    user = callback.from_user
    totem_key = callback.data.replace("contact_", "").strip()

    # Формируем текст для сотрудника зоопарка
    request_text = (
        "📩 Новый контактный запрос:\n"
        f"👤 Пользователь: {user.full_name} (ID: {user.id})\n"
        f"🐾 Тотемное животное: {totem_key}\n"
    )

    # Сохраняем запрос в файл
    contact_dir = 'data'
    contact_path = os.path.join(contact_dir, 'contact_requests.txt')

    try:
        os.makedirs(contact_dir, exist_ok=True)
        with open(contact_path, 'a', encoding='utf-8') as f:
            f.write(request_text + "\n")
        logger.info(f"Контактный запрос сохранён: user_id={user.id}, totem={totem_key}")
    except Exception as e:
        logger.exception(f"Ошибка при сохранении контактного запроса: {e}")

    # Отправляем подтверждение пользователю
    await callback.message.answer(
        "📧 Ваш запрос успешно отправлен сотрудникам Московского зоопарка! "
        "Мы свяжемся с вами в ближайшее время."
    )
    await callback.answer()