# premium.py — функции PREMIUM (v0.4.1)

from .license import has_access, PLAYEROK_URL
from .core import color
from .utils import load_json, save_json, log_info, log_warn, log_error
import json
import os

# ===== СТАРЫЕ ФУНКЦИИ (без изменений) =====

def print_table(data, headers=None, title=None):
    if not has_access("premium"):
        print(f"❌ Функция print_table доступна в TAC-PREMIUM и выше.")
        print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
        return
    if not data:
        print("Нет данных.")
        return
    if headers is None:
        if isinstance(data[0], dict):
            headers = list(data[0].keys())
        else:
            headers = [f"Колонка {i+1}" for i in range(len(data[0]))]
    col_widths = [len(str(h)) for h in headers]
    for row in data:
        if isinstance(row, dict):
            row_values = [row.get(h, "") for h in headers]
        else:
            row_values = row
        for i, val in enumerate(row_values):
            col_widths[i] = max(col_widths[i], len(str(val)))
    if title:
        print(f"\n{title}")
        print("-" * (sum(col_widths) + 3 * len(headers) + 1))
    header_line = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))
    for row in data:
        if isinstance(row, dict):
            row_values = [row.get(h, "") for h in headers]
        else:
            row_values = row
        line = " | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row_values))
        print(line)

def input_int(prompt, min_val=None, max_val=None):
    if not has_access("premium"):
        print(f"❌ Функция input_int доступна в TAC-PREMIUM и выше.")
        print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
        return None
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"❌ Значение должно быть не меньше {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"❌ Значение должно быть не больше {max_val}.")
                continue
            return value
        except ValueError:
            print("❌ Введите целое число.")

def input_choice(prompt, options):
    if not has_access("premium"):
        print(f"❌ Функция input_choice доступна в TAC-PREMIUM и выше.")
        print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
        return None
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            choice = int(input("Выберите номер: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"❌ Введите число от 1 до {len(options)}.")
        except ValueError:
            print("❌ Введите число.")

def menu(options, title="Меню"):
    if not has_access("premium"):
        print(f"❌ Функция menu доступна в TAC-PREMIUM и выше.")
        print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
        return None
    return input_choice(title, options)

# ===== НОВЫЕ JSON-ФУНКЦИИ (с правильными импортами) =====

def _get_nested_value(data, key_path):
    keys = key_path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None, f"Путь '{key_path}' не найден (остановился на '{key}')"
    return current, None

def _set_nested_value(data, key_path, value):
    keys = key_path.split(".")
    current = data
    for key in keys[:-1]:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return False, f"Путь '{key_path}' не найден (остановился на '{key}')"
    if isinstance(current, dict):
        current[keys[-1]] = value
        return True, None
    return False, "Целевой объект не является словарём"

def update_json(path, key_path, value, show_error=True):
    if not has_access("premium"):
        print(color.red(f"❌ Функция update_json доступна только в PREMIUM и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return False
    data = load_json(path, default={})
    if not data:
        return False
    success, error = _set_nested_value(data, key_path, value)
    if not success:
        if show_error:
            log_error(f"Ошибка обновления: {error}")
            if isinstance(data, dict):
                log_warn(f"Доступные ключи: {', '.join(list(data.keys())[:10])}")
        return False
    save_json(path, data)
    return True

def find_in_json(data, key, filter_value=None, current_path=""):
    if not has_access("premium"):
        print(color.red(f"❌ Функция find_in_json доступна только в PREMIUM и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return []
    results = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_path = f"{current_path}.{k}" if current_path else k
            if k == key:
                if filter_value is None or v == filter_value:
                    results.append({"path": new_path, "value": v})
            results.extend(find_in_json(v, key, filter_value, new_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{current_path}[{i}]"
            results.extend(find_in_json(item, key, filter_value, new_path))
    return results

def json_path_exists(data, key_path):
    if not has_access("premium"):
        print(color.red(f"❌ Функция json_path_exists доступна только в PREMIUM и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return False
    _, error = _get_nested_value(data, key_path)
    return error is None

def pretty_print_json(data, indent=2):
    if not has_access("premium"):
        print(color.red(f"❌ Функция pretty_print_json доступна только в PREMIUM и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            print(data)
            return
    def _print_item(item, level=0):
        prefix = "  " * level
        if isinstance(item, dict):
            for k, v in item.items():
                if isinstance(v, (dict, list)):
                    print(color.cyan(f"{prefix}{k}: "))
                    _print_item(v, level+1)
                else:
                    if isinstance(v, str):
                        print(color.green(f"{prefix}{k}: \"{v}\""))
                    elif isinstance(v, bool):
                        print(color.magenta(f"{prefix}{k}: {str(v).lower()}"))
                    elif v is None:
                        print(color.gray(f"{prefix}{k}: null"))
                    else:
                        print(color.yellow(f"{prefix}{k}: {v}"))
        elif isinstance(item, list):
            for idx, elem in enumerate(item):
                print(color.cyan(f"{prefix}[{idx}]"))
                _print_item(elem, level+1)
        else:
            print(prefix + str(item))
    _print_item(data)

def merge_json(path1, path2, output_path=None, overwrite=False):
    if not has_access("premium"):
        print(color.red(f"❌ Функция merge_json доступна только в PREMIUM и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return False
    data1 = load_json(path1)
    data2 = load_json(path2)
    if data1 is None or data2 is None:
        log_error("Один из файлов не удалось загрузить")
        return False
    def deep_merge(a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            result = a.copy()
            for key, value in b.items():
                if key in result:
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        return b if overwrite else a
    merged = deep_merge(data1, data2)
    if output_path is None:
        output_path = "merged_" + os.path.basename(path1)
    save_json(output_path, merged)
    log_info(f"Объединённый JSON сохранён в {output_path}")
    return merged

def auto_complete_json(path, partial, show_error=True):
    if not has_access("premium"):
        print(color.red(f"❌ Функция auto_complete_json доступна только в PREMIUM и выше."))
        print(color.yellow(f"👉 Приобретите подписку: {PLAYEROK_URL}"))
        return None
    data = load_json(path, default={})
    if not data:
        return None
    parts = partial.split(".")
    current = data
    for i, p in enumerate(parts[:-1]):
        if isinstance(current, dict) and p in current:
            current = current[p]
        else:
            if show_error:
                log_error(f"Путь '{'.'.join(parts[:i+1])}' не найден")
            return None
    last_part = parts[-1] if parts else ""
    if isinstance(current, dict):
        matches = [k for k in current.keys() if k.startswith(last_part)]
        if not matches:
            log_warn(f"Нет ключей, начинающихся с '{last_part}'")
            log_warn(f"Доступные ключи: {', '.join(list(current.keys())[:10])}")
            return None
        if len(matches) == 1:
            full_path = f"{'.'.join(parts[:-1])}.{matches[0]}" if parts[:-1] else matches[0]
            log_info(f"Автодополнено: {full_path}")
            return full_path
        else:
            log_info(f"Найдены варианты: {', '.join(matches)}")
            return None
    else:
        log_error("Текущий объект не является словарём")
        return None