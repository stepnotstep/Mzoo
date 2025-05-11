import json
import os
from typing import Dict, List

def load_questions() -> List[Dict]:
    """Загружает вопросы викторины из JSON-файла."""
    path = os.path.join('data', 'questions.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_animals() -> Dict[str, Dict]:
    """Загружает информацию о животных из JSON-файла."""
    path = os.path.join('data', 'animals.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)