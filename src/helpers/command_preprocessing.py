"""
This file contains functions to preprocess messages in order for them to work with both slash
commands and prefixed commands. Preprocessing has to be handled on a per command basis. Only
preprocess_command(msg) should ever be directly called.
"""

from src.helpers.global_vars import DEFAULT_PREFIX
from src.helpers.command_aliases import WEAPON_INFO_ALIASES

def process_weapon_info_command_args(args: str) -> str:
    args = args.replace("-", " ").split()
    return "_".join(args).lower()

def preprocess_command(msg: str) -> str:
    msg = msg.lower()
    noprefix = msg[2:].strip() # remove whitespace between the bot prefix and the command
    cmd = noprefix[:noprefix.index(" ")] if " " in noprefix else noprefix
    args = noprefix[noprefix.index(" "):].strip() if " " in noprefix else ""

    processed_cmd = f"{DEFAULT_PREFIX}{cmd} {args}"
    
    # weapon info
    if cmd == "weapon_info" or cmd in WEAPON_INFO_ALIASES:
        processed_args = process_weapon_info_command_args(args)
        processed_cmd = f"{DEFAULT_PREFIX}{cmd} {processed_args}"

    return processed_cmd