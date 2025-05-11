import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Получаем ссылку на прграмму опекунства
GUARDIAN_LINK = os.getenv("GUARDIANSHIP_LINK")

# Путь к JSON-файлам с данными
QUESTIONS_PATH = os.path.join("data", "questions.json")
ANIMALS_PATH = os.path.join("data", "animals.json")

# Проверка наличия необходимых файлов
REQUIRED_FILES = [QUESTIONS_PATH, ANIMALS_PATH]

for file_path in REQUIRED_FILES:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Не найден необходимый файл: {file_path}")