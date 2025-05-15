from src.helpers.global_vars import DEFAULT_PREFIX

"""
This file contains functions to preprocess messages in order for them to work with both slash
commands and prefixed commands. Preprocessing has to be handled on a per command basis. Only
preprocess_command(msg) should ever be directly called.
"""

def process_test_command(cmd: str) -> str:
    args = cmd.split(" ")
    return f"{DEFAULT_PREFIX}{args[0]} {"".join(args[1:])}"

def preprocess_command(msg: str) -> str:
    msg = msg.lower()
    cmd = msg[2:].strip() # remove whitespace between the bot prefix and the command
    
    if cmd.startswith("test"):
        msg = process_test_command(cmd)

    return msg