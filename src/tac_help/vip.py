# vip.py — функции VIP (v0.3.0)

import requests
from .license import has_access, PLAYEROK_URL

# ========== ЛОКАЛЬНЫЕ ОТВЕТЫ (доступны ВСЕМ) ==========

def _ask_local(prompt: str) -> str:
    """Локальный режим — без API, только шаблонные ответы."""
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

# ========== ОБРАБОТКА ОШИБОК API (красиво и понятно) ==========

def _format_api_error(e: Exception) -> str:
    """Превращает исключение в понятное сообщение."""
    if isinstance(e, requests.exceptions.Timeout):
        return "⏳ Превышено время ожидания. Проверьте интернет и попробуйте позже."
    if isinstance(e, requests.exceptions.ConnectionError):
        return "🔌 Нет соединения с интернетом. Проверьте подключение."
    if isinstance(e, requests.exceptions.HTTPError):
        if e.response.status_code == 401:
            return "🔑 Неверный API-ключ. Проверьте его и попробуйте снова."
        if e.response.status_code == 403:
            return "🚫 Доступ запрещён. Возможно, у вас нет прав на использование этого API."
        if e.response.status_code == 429:
            return "⏳ Слишком много запросов. Подождите немного и попробуйте снова."
        return f"⚠️ Ошибка сервера ({e.response.status_code}). Попробуйте позже."
    if isinstance(e, KeyError):
        return "⚠️ Неожиданный ответ от API. Проверьте ключ и модель."
    return f"⚠️ Неизвестная ошибка: {e}"

# ========== ОСНОВНАЯ ФУНКЦИЯ ask_ai ==========

def ask_ai(prompt: str, model: str = "deepseek", api_key: str = None, use_local: bool = False) -> str:
    """
    Универсальный запрос к ИИ-API.
    
    - Если use_local=True — возвращает локальный ответ (без API). Доступно ВСЕМ.
    - Если use_local=False и передан api_key — отправляет реальный запрос (только VIP).
    - Если use_local=False и api_key не передан — выводит инструкцию.
    """
    # Локальный режим доступен всем (без проверки VIP)
    if use_local:
        return _ask_local(prompt)

    # Реальный API — только для VIP
    if not has_access("vip"):
        return (
            "❌ Реальный ИИ-API доступен только в TAC-VIP и выше.\n"
            f"👉 Приобретите подписку: {PLAYEROK_URL}\n"
            "💡 Или используйте локальный режим: ask_ai('Привет', use_local=True)"
        )

    if not api_key:
        return (
            "🔑 Для использования реального ИИ-API укажите свой API-ключ.\n"
            "   Пример: ask_ai('Привет', api_key='sk-...')\n"
            "   Или установите переменную окружения TAC_API_KEY."
        )

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return _format_api_error(e)

# ========== ДРУГИЕ VIP-ФУНКЦИИ ==========

def summarize(text: str, max_length: int = 100) -> str:
    """Суммаризация текста (локальная, без API)."""
    if not has_access("vip"):
        return f"❌ Функция summarize доступна в TAC-VIP и выше.\n👉 {PLAYEROK_URL}"
    if len(text) <= max_length:
        return text
    return text[:max_length] + "... (сокращено)"

def fetch_json(url: str):
    """Получает JSON по URL (реальный запрос)."""
    if not has_access("vip"):
        return f"❌ Функция fetch_json доступна в TAC-VIP и выше.\n👉 {PLAYEROK_URL}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return "⏳ Превышено время ожидания. Проверьте интернет."
    except requests.exceptions.ConnectionError:
        return "🔌 Нет соединения с интернетом."
    except requests.exceptions.HTTPError as e:
        return f"⚠️ Ошибка HTTP {e.response.status_code}: {e.response.reason}"
    except Exception as e:
        return f"⚠️ Ошибка: {e}"