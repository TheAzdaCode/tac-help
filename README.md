🧠 tac-help

Универсальная Python-библиотека для разработчиков с гибкой системой лицензирования.

tac-help — это набор готовых инструментов для консольных приложений: цветной вывод, прогресс-бары, таблицы, меню, работа с JSON, логирование и даже запросы к ИИ. Всё разделено по уровням доступа: FREE → PRO → PREMIUM → VIP.

Библиотека уже опубликована на PyPI и устанавливается одной командой.

---

📦 Установка

```bash
pip install tac-help
```

После установки проверь версию:

```bash
tac-help version
```

---

🖥️ CLI-команды

Команда Описание
tac-help activate <ключ> Активировать лицензионный ключ
tac-help status Показать текущий уровень доступа
tac-help list Список функций по уровням
tac-help version Версия библиотеки

---

🧩 Уровни доступа

Уровень Что доступно
FREE color, pause, clear — всегда бесплатно
PRO progress_bar, @timer, @retry
PREMIUM print_table, input_int, input_choice, menu
VIP ask_ai (локальный и реальный ИИ), summarize, fetch_json

---

🎨 Использование в коде

```python
from tac_help import color, clear, pause, progress_bar, print_table, ask_ai, log_info

clear()
print(color.bold_green("Добро пожаловать в tac-help!"))

# Прогресс-бар (PRO)
for _ in progress_bar(range(10), desc="Загрузка"):
    pass

# Таблица (PREMIUM)
data = [{"Имя": "Арсений", "Роль": "Создатель"}]
print_table(data, title="Команда")

# ИИ — локальный режим (доступен всем)
print(ask_ai("Привет!", use_local=True))

# Логирование
log_info("Скрипт завершён")

pause()
```

---

🤖 ask_ai — работа с ИИ

Локальный режим (демо, доступен всем)

```python
print(ask_ai("Как дела?", use_local=True))
# → "У меня всё отлично! А у тебя?"
```

Реальный ИИ-API (только VIP)

Укажи свой API-ключ (например, DeepSeek) и получи реальный ответ:

```python
print(ask_ai("Привет!", api_key="sk-..."))
```

Если ключ не указан — библиотека подскажет, что делать.

Все ошибки API обрабатываются и выводятся понятными сообщениями:

· ⏳ Превышено время ожидания
· 🔑 Неверный API-ключ
· 🔌 Нет соединения с интернетом
· и другие.

---

🛠️ Дополнительные утилиты

```python
from tac_help import load_json, save_json, log_info, log_warn, log_error

save_json({"key": "value"}, "data.json")
data = load_json("data.json")

log_info("Информация")
log_warn("Предупреждение")
log_error("Ошибка")
```

---

🔐 Управление ключами (для владельца)

Для администраторов есть отдельный скрипт key_manager.py. Он позволяет:

· Создавать, удалять, изменять ключи
· Включать/выключать ключи (поле active)
· Управлять пасхалкой «Найс тру!»
· Просматривать просроченные ключи

Запуск:

```bash
python key_manager.py
```

---

📄 Лицензия

MIT © TheAzdaCode

---

🌐 Ссылки

· GitHub
· PyPI
· Сайт TAC
· Магазин ключей на Playerok

---

Сделано с ♥️ командой TAC
The Azda Company — мы создаём, потому что нам интересно.
