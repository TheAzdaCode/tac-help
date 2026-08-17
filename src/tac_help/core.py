# core.py — базовые функции FREE (v0.4.0)

import os
import time
import sys
from .license import PLAYEROK_URL

# ===== СТАРЫЕ ФУНКЦИИ (color, clear, pause) =====

class _Color:
    def __init__(self, prefix="", suffix=""):
        self.prefix = prefix
        self.suffix = suffix

    def __call__(self, text):
        return f"{self.prefix}{text}{self.suffix}"

class _Colors:
    def __getattr__(self, name):
        codes = {
            "red": "\033[91m", "green": "\033[92m",
            "yellow": "\033[93m", "blue": "\033[94m",
            "magenta": "\033[95m", "cyan": "\033[96m",
            "white": "\033[97m", "reset": "\033[0m",
            "bold": "\033[1m", "italic": "\033[3m",
            "underline": "\033[4m",
            "bg_red": "\033[101m", "bg_green": "\033[102m",
            "bg_yellow": "\033[103m", "bg_blue": "\033[104m",
            "bg_magenta": "\033[105m", "bg_cyan": "\033[106m",
            "bg_white": "\033[107m",
        }
        if name in codes:
            return _Color(codes[name], codes["reset"])
        parts = name.split('_')
        if len(parts) == 2 and parts[0] in ["bold", "italic", "underline"]:
            style = codes.get(parts[0])
            color_code = codes.get(parts[1])
            if style and color_code:
                return _Color(style + color_code, codes["reset"])
        raise AttributeError(f"Цвет или стиль '{name}' не найден")

color = _Colors()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nНажми Enter чтобы продолжить...")

# ===== НОВЫЕ FREE-ФУНКЦИИ =====

def confirm(prompt, default=False):
    """Диалог Да/Нет (возвращает True/False)."""
    hint = " [y/N]: " if default is False else " [Y/n]: "
    response = input(prompt + hint).strip().lower()
    if response in ("y", "yes", "да", "д"):
        return True
    if response in ("n", "no", "нет", "н"):
        return False
    return default

def input_timeout(prompt, timeout=5):
    """Ввод с таймаутом (если не введено за N секунд — пропускает)."""
    print(prompt, end=" ", flush=True)
    # Простая версия без select (работает везде)
    import threading
    result = [None]
    def get_input():
        result[0] = sys.stdin.readline().strip()
    thread = threading.Thread(target=get_input, daemon=True)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        print("\n⏳ Время вышло")
        return None
    return result[0]

def spinner(text="Загрузка", duration=3):
    """Показывает анимированный спиннер в консоли."""
    symbols = ['|', '/', '-', '\\']
    for i in range(duration * 10):
        print(f"\r{text} {symbols[i % 4]}", end="")
        time.sleep(0.1)
    print("\r" + " " * (len(text) + 2), end="\r")