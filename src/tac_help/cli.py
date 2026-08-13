# cli.py — интерфейс командной строки для tac-help

import sys
import argparse
from .license import activate, get_tier, has_access
from .core import color

def main():
    parser = argparse.ArgumentParser(description="TAC-Help — управление лицензией и утилитами")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Команда activate
    activate_parser = subparsers.add_parser("activate", help="Активировать лицензионный ключ")
    activate_parser.add_argument("key", help="Ключ активации (например, TAC-PRO-XXXX-YYYY)")

    # Команда status
    status_parser = subparsers.add_parser("status", help="Показать текущий уровень доступа")

    # Команда list
    list_parser = subparsers.add_parser("list", help="Показать доступные функции по уровням")

    # Команда help (уже есть по умолчанию)

    args = parser.parse_args()

    if args.command == "activate":
        success, msg = activate(args.key)
        if success:
            print(color.green(f"✅ {msg}"))
        else:
            print(color.red(f"❌ {msg}"))

    elif args.command == "status":
        tier = get_tier()
        print(color.cyan(f"Текущий уровень доступа: {tier}"))
        if tier != "free":
            print(color.green("✅ Действительная подписка"))
        else:
            print(color.yellow("⚠️ Бесплатная версия. Приобретите подписку для расширенных функций."))

    elif args.command == "list":
        print(color.bold_cyan("📋 Доступные функции по уровням:"))
        print(color.green("FREE: color, pause, clear"))
        print(color.yellow("PRO: progress_bar, timer, retry"))
        print(color.magenta("PREMIUM: print_table, input_int, input_choice, menu"))
        print(color.cyan("VIP: ask_ai, summarize, fetch_json"))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()