"""
This file contains functions to preprocess messages in order for them to work with both slash
commands and prefixed commands. Preprocessing has to be handled on a per command basis. Only
preprocess_command(msg) should ever be directly called.
"""

from src.helpers.global_vars import DEFAULT_PREFIX
from src.helpers.command_aliases import WEAPON_INFO_ALIASES, WEAPON_TIPS_ALIASES, WEAPON_TREE_ALIASES, XP_ALIASES

#region processing functions

# For commands: weapon_info, weapon_tips, weapon_tree
# 1 arg expected: weapon name
def process_weapon_name_in_command_args(args: str) -> str:
    args = args.replace("-", " ").split() #removes consecutive spaces, replaces with a single _
    return "_".join(args)


#for command: xp
# 1 optional arg expected: None | level
def process_xp_command_args(args: str) -> str:
    return args.replace(" ", "") # removes spaces for star levels 

#endregion

def preprocess_command(msg: str) -> str:
    msg = msg.lower()
    noprefix = msg[2:].strip() # remove whitespace between the bot prefix and the command
    cmd = noprefix[:noprefix.index(" ")] if " " in noprefix else noprefix
    args = noprefix[noprefix.index(" "):].strip() if " " in noprefix else ""

    processed_cmd = f"{DEFAULT_PREFIX}{cmd} {args}"
    
    # weapon info
    # weapon tips
    if cmd == "weapon_info" or cmd in WEAPON_INFO_ALIASES or cmd == "weapon_tips" or cmd in WEAPON_TIPS_ALIASES or cmd == "weapon_tree" or cmd in WEAPON_TREE_ALIASES:
        processed_args = process_weapon_name_in_command_args(args)
        processed_cmd = f"{DEFAULT_PREFIX}{cmd} {processed_args}"

        # Hard coded replacements for weapon aliases
        processed_cmd = processed_cmd.replace("bow_and_arrow", "bow_&_arrow")
    
    # xp
    if cmd == "xp" or cmd in XP_ALIASES:
        processed_args = process_xp_command_args(args)
        processed_cmd = f"{DEFAULT_PREFIX}{cmd} {processed_args}"

    return processed_cmd