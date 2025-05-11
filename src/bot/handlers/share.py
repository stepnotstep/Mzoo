import logging
from aiogram import Router, F, types

router = Router()
logger = logging.getLogger("zoo_bot.handlers.sharing")

@router.callback_query(F.data.startswith("share_"))
async def handle_share_request(callback: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки «📢 Поделиться».
    Отправляет пользователю текстовое сообщение,
    которое он может легко переслать или опубликовать.
    """
    user = callback.from_user
    totem_key = callback.data.replace("share_", "").strip()

    logger.info(f"Пользователь {user.id} выбрал поделиться результатом: {totem_key}")

    # Получаем username бота для формирования ссылки
    try:
        bot_info = await callback.bot.get_me()
        bot_username = bot_info.username.replace("_", r"\_")
    except Exception as e:
        logger.warning(f"Не удалось получить имя бота: {e}")
        bot_username = "MZoo_Bot"


    # Формируем текст с подсказкой как опубликовать
    message_text = (
        "📲 Чтобы поделиться результатом:\n"
        "1. Нажмите на сообщение выше.\n"
        "2. Нажмите «Переслать».\n"
        "3. Выберите чат или контакт.\n"
        "4. Или скопируйте ссылку на бота и отправьте в любом мессенджере:\n"
        f"https://t.me/{bot_username}"
    )

    # Вариант: отправляем сообщение, которое можно переслать
    await callback.message.answer(
        f"{message_text}\n",
        parse_mode="Markdown"
    )

    await callback.answer()
