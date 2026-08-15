# cli.py — интерфейс командной строки для tac-help (v0.3.0)

import sys
import argparse
from .license import activate, get_tier, has_access
from .core import color

def main():
    parser = argparse.ArgumentParser(description="TAC-Help — управление лицензией и утилитами")
    subparsers = parser.add_subparsers(dest="command", required=True)

    activate_parser = subparsers.add_parser("activate", help="Активировать лицензионный ключ")
    activate_parser.add_argument("key", help="Ключ активации (например, TAC-PRO-XXXX-YYYY)")

    status_parser = subparsers.add_parser("status", help="Показать текущий уровень доступа")
    list_parser = subparsers.add_parser("list", help="Показать доступные функции по уровням")
    version_parser = subparsers.add_parser("version", help="Показать версию библиотеки")

    toggle_key_parser = subparsers.add_parser("toggle-key", help="Включить/выключить ключ (только владелец)")
    toggle_key_parser.add_argument("key", help="Ключ для переключения")

    toggle_nice_parser = subparsers.add_parser("toggle-nice-try", help="Включить/выключить пасхалку 'Найс тру!' (только владелец)")

    keys_parser = subparsers.add_parser("keys", help="Показать все ключи с их статусами (только владелец)")

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

    elif args.command == "version":
        from . import __version__
        print(f"tac-help версия {__version__}")

    elif args.command in ("toggle-key", "toggle-nice-try", "keys"):
        print(color.yellow("Эта команда доступна только через key_manager.py."))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()