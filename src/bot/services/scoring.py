from collections import defaultdict
from typing import List, Dict, Optional, Tuple

def calculate_scores(answer_weights: List[List[str]]) -> Dict[str, int]:
    """
    Рассчитывает общий вес для каждого животного на основе ответов пользователя.
    Каждое совпадение увеличивает счетчик животного.
    """
    scores = defaultdict(int)
    for weights in answer_weights:
        for animal in weights:
            scores[animal] += 1
    return dict(scores)

def determine_top_animal(scores: Dict[str, int]) -> Optional[Tuple[str, int]]:
    """
    Определяет животное с наибольшим количеством очков.
    Если список пуст — возвращает None.
    """
    if not scores:
        return None
    return max(scores.items(), key=lambda item: item[1])