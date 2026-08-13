🧠 tac-help

Универсальная библиотека для разработчиков с системой лицензирования.

tac-help — это Python-библиотека, которая объединяет полезные утилиты для консольных приложений: цветной вывод, прогресс-бары, таблицы, меню, логирование, работу с JSON и многое другое. Всё с продуманной системой доступа: FREE → PRO → PREMIUM → VIP.

--- 

📦 Установка

```bash
pip install tac-help
```

---

🖥️ CLI-команды

После установки доступны команды в терминале:

```bash
tac-help activate <ключ>   # активировать лицензионный ключ
tac-help status             # показать текущий уровень доступа
tac-help list               # список функций по уровням
```

---

📖 Использование в коде

```python
from tac_help import color, progress_bar, print_table, ask_ai, log_info

# Цветной вывод
print(color.green("Привет, TAC!"))

# Прогресс-бар (PRO)
for _ in progress_bar(range(10), desc="Загрузка"):
    pass

# Таблица (PREMIUM)
data = [{"Имя": "Арсений", "Возраст": 12}]
print_table(data, title="Команда")

# Локальный ИИ-ответ (VIP)
print(ask_ai("Что такое TAC?"))

# Логирование
log_info("Скрипт завершён")
```

---

🧩 Уровни доступа

Уровень Функции
FREE color, pause, clear
PRO progress_bar, timer, retry
PREMIUM print_table, input_int, input_choice, menu
VIP ask_ai, summarize, fetch_json

Все платные функции при отсутствии ключа выводят сообщение с предложением приобрести подписку.

---

🛠️ Дополнительные утилиты

· load_json(path) — загрузить JSON из файла
· save_json(data, path) — сохранить JSON
· log_info(msg), log_warn(msg), log_error(msg) — цветное логирование с временем

---

📄 Лицензия 

MIT © TheAzdaCode

---

🌐 Ссылки

· GitHub
· PyPI
· Сайт TAC

---

Сделано с ♥️ командой TAC
