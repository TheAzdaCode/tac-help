# utils.py — утилиты (логирование, работа с JSON)

import json
import os
from datetime import datetime
from .core import color

def log_info(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(color.cyan(f"[{ts}] ℹ️ {msg}"))

def log_warn(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(color.yellow(f"[{ts}] ⚠️ {msg}"))

def log_error(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(color.red(f"[{ts}] ❌ {msg}"))

def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data, indent=2):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except:
        return False