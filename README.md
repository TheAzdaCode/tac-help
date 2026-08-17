🧠 tac-help

Универсальная Python-библиотека для разработчиков с гибкой системой лицензирования.

tac-help — это набор готовых инструментов для консольных приложений: цветной вывод, прогресс-бары, таблицы, меню, работа с JSON, логирование, запросы к ИИ и многое другое. Всё разделено по уровням доступа: FREE → PRO → PREMIUM → VIP.

Библиотека опубликована на PyPI и устанавливается одной командой.

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

🧩 Уровни доступа и функции

🔓 FREE (доступны всегда)

· color — цветной вывод (red, green, blue, yellow, cyan, magenta, white, bold, italic, underline, bg_*)
· clear() — очистка экрана
· pause() — ожидание нажатия Enter
· confirm(prompt, default=False) — диалог Да/Нет
· input_timeout(prompt, timeout=5) — ввод с таймаутом
· spinner(text, duration=3) — анимация загрузки

🟡 PRO (нужен PRO-ключ)

· progress_bar(iterable, desc="", length=30) — прогресс-бар
· @timer — замер времени выполнения функции
· @retry(times=3, delay=1) — повтор при ошибке
· backup_json(path, backup_dir=None) — создание резервной копии JSON
· diff_json(path1, path2) — сравнение двух JSON

🟠 PREMIUM (нужен PREMIUM-ключ)

· print_table(data, headers=None, title=None) — вывод таблицы
· input_int(prompt, min_val=None, max_val=None) — ввод числа с проверкой
· input_choice(prompt, options) — выбор из списка по номеру
· menu(options, title="Меню") — интерактивное меню
· update_json(path, key_path, value) — обновление значения по пути в JSON
· find_in_json(data, key, filter_value=None) — рекурсивный поиск по ключу
· json_path_exists(data, key_path) — проверка существования пути
· pretty_print_json(data, indent=2) — красивый цветной вывод JSON
· merge_json(path1, path2, output_path=None, overwrite=False) — объединение двух JSON
· auto_complete_json(path, partial) — интерактивное автодополнение пути

🔴 VIP (нужен VIP-ключ)

· ask_ai(prompt, api_key=None, use_local=False) — запрос к ИИ (локальный или через API)
· summarize(text, max_length=100) — сокращение текста
· fetch_json(url) — получение данных по URL
· get_tariff_data(path="keys.json") — извлечение всех тарифов
· get_tier_info(tier, path="keys.json") — информация об уровне
· get_tier_price(tier, days, path="keys.json") — цена для уровня на N дней
· format_tariff_list(path="keys.json") — красивый вывод тарифов
· set_tier_price(tier, days, price, path="prices.json") — установка цены
· @log_call — логирование вызова функции
· @timeout(seconds) — ограничение времени выполнения
· @cache — кеширование результата функции

---

🛠️ Утилиты (доступны всегда)

```python
from tac_help import load_json, save_json, log_info, log_warn, log_error
```

· load_json(path, default=None) — загрузка JSON
· save_json(path, data, indent=2) — сохранение JSON
· log_info(msg), log_warn(msg), log_error(msg) — цветное логирование с временем

---

🎨 Пример использования

```python
from tac_help import color, clear, pause, confirm, spinner, progress_bar, print_table, ask_ai, log_info

clear()
print(color.bold_green("Добро пожаловать в TAC-HELP!"))

spinner("Загрузка", 2)

if confirm("Показать прогресс-бар?", default=True):
    for _ in progress_bar(range(10), desc="Обработка"):
        pass

data = [{"Имя": "Арсений", "Роль": "Создатель"}]
print_table(data, title="Команда")

print(ask_ai("Привет!", use_local=True))

pause()
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
