# premium.py — функции PREMIUM

from .license import has_access, PLAYEROK_URL

def print_table(data, headers=None, title=None):
    """Вывод данных в виде таблицы. Доступен в PREMIUM и выше."""
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

    # Вычисляем ширину колонок
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

    # Шапка
    header_line = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))

    # Данные
    for row in data:
        if isinstance(row, dict):
            row_values = [row.get(h, "") for h in headers]
        else:
            row_values = row
        line = " | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row_values))
        print(line)

def input_int(prompt, min_val=None, max_val=None):
    """Ввод целого числа с проверкой диапазона. Доступен в PREMIUM и выше."""
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
    """Выбор из списка по номеру. Доступен в PREMIUM и выше."""
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
    """Вывод меню с выбором. Доступен в PREMIUM и выше."""
    if not has_access("premium"):
        print(f"❌ Функция menu доступна в TAC-PREMIUM и выше.")
        print(f"👉 Приобретите подписку: {PLAYEROK_URL}")
        return None
    return input_choice(title, options)