# pro.py — функции PRO (v0.4.3)

import time
import os
import json
from .license import has_access, PLAYEROK_URL
from .core import color
from .utils import load_json, save_json, log_info, log_warn, log_error

# ===== СТАРЫЕ ФУНКЦИИ =====

def progress_bar(iterable, desc="Progress", length=30):
    if not has_access("pro"):
        print(f"❌ Функция progress_bar доступна в TAC-PRO и выше.")
        print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
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
            print(f"❌ Декоратор timer доступен в TAC-PRO и выше.")
            print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
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
                print(f"❌ Декоратор retry доступен в TAC-PRO и выше.")
                print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
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

# ===== НОВЫЕ PRO-ФУНКЦИИ =====

def backup_json(path, backup_dir=None):
    if not has_access("pro"):
        print(color.red(f"❌ Функция backup_json доступна только в PRO и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return False
    if not os.path.exists(path):
        log_error(f"Файл '{path}' не найден")
        return False
    if backup_dir is None:
        backup_dir = os.path.dirname(path)
    os.makedirs(backup_dir, exist_ok=True)
    base = os.path.basename(path)
    name, ext = os.path.splitext(base)
    backup_path = os.path.join(backup_dir, f"{name}_backup{ext}")
    try:
        with open(path, "r", encoding="utf-8") as f_in:
            with open(backup_path, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())
        log_info(f"Резервная копия создана: {backup_path}")
        return True
    except Exception as e:
        log_error(f"Ошибка создания резервной копии: {e}")
        return False

def diff_json(path1, path2):
    if not has_access("pro"):
        print(color.red(f"❌ Функция diff_json доступна только в PRO и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return
    def load_json_safe(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            log_error(f"Не удалось загрузить {p}")
            return None
    data1 = load_json_safe(path1)
    data2 = load_json_safe(path2)
    if data1 is None or data2 is None:
        return
    def compare_dict(d1, d2, path=""):
        diff = []
        all_keys = set(d1.keys()) | set(d2.keys())
        for key in all_keys:
            current_path = f"{path}.{key}" if path else key
            if key not in d1:
                diff.append(f"➕ {current_path}: только во втором файле")
            elif key not in d2:
                diff.append(f"➖ {current_path}: только в первом файле")
            elif isinstance(d1[key], dict) and isinstance(d2[key], dict):
                diff.extend(compare_dict(d1[key], d2[key], current_path))
            elif d1[key] != d2[key]:
                diff.append(f"🔄 {current_path}: {d1[key]} → {d2[key]}")
        return diff
    differences = compare_dict(data1, data2)
    if not differences:
        log_info("✅ Файлы идентичны")
    else:
        log_warn(f"Найдены различия ({len(differences)}):")
        for d in differences[:20]:
            print(d)
        if len(differences) > 20:
            print(f"... и ещё {len(differences)-20} различий")