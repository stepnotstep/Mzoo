import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from src.bot.core.logger import setup_logger
from src.bot.core.config import BOT_TOKEN
from src.bot.router import router

# Загружаем переменные окружения из .env
load_dotenv()

# Настраиваем логгер
logger = setup_logger("zoo_bot")

async def main():
    """
    Точка входа в бота:
    — инициализирует бота,
    — подключает роутер,
    — запускает polling.
    """
    logger.info("🚀 Бот начинает работу...")

    # Проверяем наличие токена
    if not BOT_TOKEN:
        logger.critical("❌ Не указан BOT_TOKEN. Проверьте файл .env")
        raise ValueError("BOT_TOKEN не найден. Убедитесь, что он указан в .env")

    # Инициализируем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем главный роутер
    dp.include_router(router)

    try:
        logger.info("🤖 Бот запущен и готов к работе!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"🚨 Произошла ошибка при запуске бота: {e}")
    finally:
        # Корректно закрываем сессию бота
        logger.info("🛑 Бот остановлен.")
        await bot.session.close()

if __name__ == "__main__":
    # Запуск асинхронного цикла
    asyncio.run(main())