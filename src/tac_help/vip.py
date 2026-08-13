# vip.py — функции VIP (без реального API)

import requests
from .license import has_access, PLAYEROK_URL

def ask_ai(prompt, model="local"):
    """
    Отвечает на вопрос, используя локальные шаблоны.
    Доступен в VIP и выше.
    """
    if not has_access("vip"):
        print(f"❌ Функция ask_ai доступна в TAC-VIP и выше.")
        print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
        return None

    # Локальные шаблоны (без API)
    patterns = {
        "привет": "Привет! Чем могу помочь?",
        "как дела": "У меня всё отлично! А у тебя?",
        "что такое tac-help": "TAC-Help — это библиотека для разработчиков с системой лицензирования.",
        "погода": "Я не знаю погоду, но могу подсказать, как её узнать через API.",
    }
    for key, answer in patterns.items():
        if key in prompt.lower():
            return answer

    return f"🤖 Я пока не знаю ответа на '{prompt}', но скоро научусь!"

def summarize(text, max_length=100):
    """
    Сокращает текст до указанной длины (без API).
    Доступен в VIP и выше.
    """
    if not has_access("vip"):
        print(f"❌ Функция summarize доступна в TAC-VIP и выше.")
        print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
        return None

    if len(text) <= max_length:
        return text
    return text[:max_length] + "... (сокращено)"

def fetch_json(url):
    """
    Получает JSON по URL (реальный запрос).
    Доступен в VIP и выше.
    """
    if not has_access("vip"):
        print(f"❌ Функция fetch_json доступна в TAC-VIP и выше.")
        print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
        return None

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Ошибка при запросе: {e}")
        return None