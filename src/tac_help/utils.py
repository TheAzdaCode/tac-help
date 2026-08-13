# utils.py — полезные утилиты и цветное логирование

import json
import os
from datetime import datetime
from .core import color

def load_json(path, default=None):
    """Загружает JSON из файла. Если файла нет — возвращает default."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(color.red(f"❌ Ошибка загрузки {path}: {e}"))
        return default

def save_json(data, path, indent=2):
    """Сохраняет данные в JSON-файл с форматированием."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        print(color.green(f"✅ Данные сохранены в {path}"))
        return True
    except OSError as e:
        print(color.red(f"❌ Ошибка сохранения {path}: {e}"))
        return False

def log_info(msg):
    """Выводит информационное сообщение с временем."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(color.cyan(f"[{ts}] ℹ️ {msg}"))

def log_warn(msg):
    """Выводит предупреждение с временем."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(color.yellow(f"[{ts}] ⚠️ {msg}"))

def log_error(msg):
    """Выводит ошибку с временем."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(color.red(f"[{ts}] ❌ {msg}"))