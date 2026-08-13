# core.py — базовые функции (бесплатно)

import os

class _Color:
    def __init__(self, prefix="", suffix=""):
        self.prefix = prefix
        self.suffix = suffix

    def __call__(self, text):
        return f"{self.prefix}{text}{self.suffix}"

class _Colors:
    def __getattr__(self, name):
        codes = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "reset": "\033[0m",
            "bold": "\033[1m",
            "italic": "\033[3m",
            "underline": "\033[4m",
            "bg_red": "\033[101m",
            "bg_green": "\033[102m",
            "bg_yellow": "\033[103m",
            "bg_blue": "\033[104m",
            "bg_magenta": "\033[105m",
            "bg_cyan": "\033[106m",
            "bg_white": "\033[107m",
        }
        if name in codes:
            return _Color(codes[name], codes["reset"])
        parts = name.split('_')
        if len(parts) == 2 and parts[0] in ["bold", "italic", "underline"]:
            style = codes.get(parts[0])
            color = codes.get(parts[1])
            if style and color:
                return _Color(style + color, codes["reset"])
        raise AttributeError(f"Цвет или стиль '{name}' не найден")

color = _Colors()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nНажми Enter чтобы продолжить...")