from .core import color, pause, clear, confirm, input_timeout, spinner
from .license import activate, get_tier, has_access, set_license_key
from .pro import progress_bar, timer, retry, backup_json, diff_json
from .premium import (
    print_table, input_int, input_choice, menu,
    update_json, find_in_json, json_path_exists,
    pretty_print_json, merge_json, auto_complete_json
)
from .vip import (
    ask_ai, summarize, fetch_json,
    get_tariff_data, get_tier_info, get_tier_price,
    format_tariff_list, set_tier_price,
    log_call, timeout, cache
)
from .utils import load_json, save_json, log_info, log_warn, log_error
from .cli import main as cli_main

__version__ = "0.4.4"
__all__ = [
    "color", "pause", "clear",
    "confirm", "input_timeout", "spinner",
    "activate", "get_tier", "has_access", "set_license_key",
    "progress_bar", "timer", "retry",
    "backup_json", "diff_json",
    "print_table", "input_int", "input_choice", "menu",
    "update_json", "find_in_json", "json_path_exists",
    "pretty_print_json", "merge_json", "auto_complete_json",
    "ask_ai", "summarize", "fetch_json",
    "get_tariff_data", "get_tier_info", "get_tier_price",
    "format_tariff_list", "set_tier_price",
    "log_call", "timeout", "cache",
    "load_json", "save_json", "log_info", "log_warn", "log_error",
    "cli_main",
]