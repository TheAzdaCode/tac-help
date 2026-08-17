# vip.py — функции VIP (v0.4.0)

import requests
import json
import time
import signal
from .license import has_access, PLAYEROK_URL
from .core import color, log_info, log_warn, log_error
from .utils import load_json, save_json

# ===== СТАРЫЕ ФУНКЦИИ (ask_ai, summarize, fetch_json) =====

def _ask_local(prompt):
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

def _format_api_error(e):
    if isinstance(e, requests.exceptions.Timeout):
        return "⏳ Превышено время ожидания. Проверьте интернет."
    if isinstance(e, requests.exceptions.ConnectionError):
        return "🔌 Нет соединения с интернетом."
    if isinstance(e, requests.exceptions.HTTPError):
        if e.response.status_code == 401:
            return "🔑 Неверный API-ключ."
        if e.response.status_code == 403:
            return "🚫 Доступ запрещён."
        if e.response.status_code == 429:
            return "⏳ Слишком много запросов."
        return f"⚠️ Ошибка сервера ({e.response.status_code})."
    if isinstance(e, KeyError):
        return "⚠️ Неожиданный ответ от API."
    return f"⚠️ Неизвестная ошибка: {e}"

def ask_ai(prompt, model="deepseek", api_key=None, use_local=False):
    if use_local:
        return _ask_local(prompt)
    if not has_access("vip"):
        return (f"❌ Реальный ИИ-API доступен только в TAC-VIP и выше.\n"
                f"👉 {PLAYEROK_URL}\n"
                "💡 Или используйте локальный режим: ask_ai('Привет', use_local=True)")
    if not api_key:
        return ("🔑 Для использования реального ИИ-API укажите свой API-ключ.\n"
                "   Пример: ask_ai('Привет', api_key='sk-...')")
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7},
            timeout=10
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return _format_api_error(e)

def summarize(text, max_length=100):
    if not has_access("vip"):
        return f"❌ Функция summarize доступна в TAC-VIP и выше.\n👉 {PLAYEROK_URL}"
    if len(text) <= max_length:
        return text
    return text[:max_length] + "... (сокращено)"

def fetch_json(url):
    if not has_access("vip"):
        return f"❌ Функция fetch_json доступна в TAC-VIP и выше.\n👉 {PLAYEROK_URL}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return _format_api_error(e)

# ===== НОВЫЕ VIP-ФУНКЦИИ (ТАРИФЫ И ДЕКОРАТОРЫ) =====

def get_tariff_data(path="keys.json"):
    if not has_access("vip"):
        print(color.red(f"❌ Функция get_tariff_data доступна только в VIP и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return {}
    data = load_json(path)
    if not data:
        return {}
    tariffs = {}
    tiers = ["free", "pro", "premium", "vip"]
    for tier in tiers:
        keys = find_in_json(data, "tier", filter_value=tier)
        if keys:
            sample = keys[0]
            expires = data.get("keys", {}).get(sample["path"].split(".")[-1], {}).get("expires", "never")
            tariffs[tier] = {
                "tier": tier,
                "example_key": sample["path"],
                "expires": expires,
                "active": data.get("keys", {}).get(sample["path"].split(".")[-1], {}).get("active", True)
            }
    return tariffs

def get_tier_info(tier, path="keys.json"):
    if not has_access("vip"):
        print(color.red(f"❌ Функция get_tier_info доступна только в VIP и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return None
    tariffs = get_tariff_data(path)
    return tariffs.get(tier)

def get_tier_price(tier, days, path="keys.json"):
    if not has_access("vip"):
        print(color.red(f"❌ Функция get_tier_price доступна только в VIP и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return None
    prices = {
        ("pro", 30): 90, ("pro", 60): 150, ("pro", 90): 220,
        ("pro", 180): 390, ("pro", 365): 690,
        ("premium", 30): 190, ("premium", 60): 320, ("premium", 90): 390,
        ("premium", 180): 690, ("premium", 365): 1290,
        ("vip", 30): 390, ("vip", 60): 650, ("vip", 90): 690,
        ("vip", 180): 1290, ("vip", 365): 2490,
    }
    return prices.get((tier, days), None)

def format_tariff_list(path="keys.json"):
    if not has_access("vip"):
        print(color.red(f"❌ Функция format_tariff_list доступна только в VIP и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return
    tariffs = get_tariff_data(path)
    if not tariffs:
        log_error("Нет данных о тарифах")
        return
    print(color.bold_cyan("\n📋 ДОСТУПНЫЕ ТАРИФЫ:"))
    print("=" * 50)
    for tier, info in tariffs.items():
        tier_color = {
            "free": color.green, "pro": color.yellow,
            "premium": color.magenta, "vip": color.cyan
        }.get(tier, color.white)
        print(tier_color(f"  {tier.upper()}:"))
        print(f"    Ключ: {info['example_key']}")
        print(f"    Срок: {info['expires']}")
        print(f"    Активен: {'✅' if info['active'] else '❌'}")
        for days in [30, 60, 90, 180, 365]:
            price = get_tier_price(tier, days)
            if price:
                print(f"    {days} дней: {price} ₽")
        print()

def set_tier_price(tier, days, price, path="prices.json"):
    if not has_access("vip"):
        print(color.red(f"❌ Функция set_tier_price доступна только в VIP и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return False
    prices = load_json(path, default={})
    if "prices" not in prices:
        prices["prices"] = {}
    if tier not in prices["prices"]:
        prices["prices"][tier] = {}
    prices["prices"][tier][str(days)] = price
    save_json(path, prices)
    log_info(f"Цена для {tier} на {days} дней установлена: {price} ₽")
    return True

# ===== ДЕКОРАТОРЫ VIP =====

def log_call(func):
    if not has_access("vip"):
        def wrapper(*args, **kwargs):
            print(color.red("❌ Декоратор @log_call доступен только в VIP и выше."))
            return func(*args, **kwargs)
        return wrapper
    def wrapper(*args, **kwargs):
        log_info(f"Вызов {func.__name__} с аргументами: {args}, {kwargs}")
        result = func(*args, **kwargs)
        log_info(f"Результат {func.__name__}: {result}")
        return result
    return wrapper

def timeout(seconds):
    if not has_access("vip"):
        def decorator(func):
            def wrapper(*args, **kwargs):
                print(color.red("❌ Декоратор @timeout доступен только в VIP и выше."))
                return func(*args, **kwargs)
            return wrapper
        return decorator
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, lambda signum, frame: (_ for _ in ()).throw(TimeoutError(f"Превышено время выполнения ({seconds} сек.)")))
            signal.alarm(seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
        return wrapper
    return decorator

def cache(func):
    if not has_access("vip"):
        def wrapper(*args, **kwargs):
            print(color.red("❌ Декоратор @cache доступен только в VIP и выше."))
            return func(*args, **kwargs)
        return wrapper
    cache_dict = {}
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key in cache_dict:
            log_info(f"Кеш: возвращаем сохранённый результат для {func.__name__}")
            return cache_dict[key]
        result = func(*args, **kwargs)
        cache_dict[key] = result
        log_info(f"Кеш: сохранён результат {func.__name__}")
        return result
    return wrapper