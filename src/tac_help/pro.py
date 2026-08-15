# pro.py — функции PRO (v0.3.0)

import time
from .license import has_access, PLAYEROK_URL

def progress_bar(iterable, desc="Progress", length=30):
    if not has_access("pro"):
        print(
            f"❌ Функция progress_bar доступна в TAC-PRO и выше.\n"
            f"👉 Приобретите подписку: {PLAYEROK_URL}"
        )
        return iterable
    total = len(iterable)
    for i, item in enumerate(iterable):
        percent = (i + 1) / total * 100
        filled = int(length * (i + 1) / total)
        bar = "█" * filled + "░" * (length - filled)
        print(f"\r{desc}: [{bar}] {percent:.1f}%", end="")
        yield item
    print()

def timer(func):
    if not has_access("pro"):
        def wrapper(*args, **kwargs):
            print(
                f"❌ Декоратор timer доступен в TAC-PRO и выше.\n"
                f"👉 Приобретите подписку: {PLAYEROK_URL}"
            )
            return func(*args, **kwargs)
        return wrapper
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱️ {func.__name__} выполнен за {elapsed:.3f} сек.")
        return result
    return wrapper

def retry(times=3, delay=1):
    if not has_access("pro"):
        def decorator(func):
            def wrapper(*args, **kwargs):
                print(
                    f"❌ Декоратор retry доступен в TAC-PRO и выше.\n"
                    f"👉 Приобретите подписку: {PLAYEROK_URL}"
                )
                return func(*args, **kwargs)
            return wrapper
        return decorator
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times:
                        raise
                    print(f"⚠️ Попытка {attempt} не удалась. Повтор через {delay} сек...")
                    time.sleep(delay)
        return wrapper
    return decorator