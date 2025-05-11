from aiogram import Router

from src.bot.handlers import (
    share,
    start,
    quiz,
    result,
    feedback,
    contact,
    share,
    test
)

# Создаём главный роутер
router = Router()

# Регистрируем все модули-обработчики
router.include_router(start.router)
router.include_router(quiz.router)
router.include_router(result.router)
router.include_router(feedback.router)
router.include_router(contact.router)
router.include_router(share.router)
router.include_router(test.router)