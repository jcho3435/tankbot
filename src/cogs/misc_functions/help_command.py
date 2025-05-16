import discord

from src.helpers.global_vars import DEFAULT_PREFIX

async def help_command(self, interaction: discord.Interaction, command: str = None):
    
    help_command = self.bot.help_command

    class FakeContext: # fake context object to trick fancyhelp into working
        def __init__(self, interaction: discord.Interaction):
            self.interaction = interaction
            self.bot = interaction.client
            self.channel = interaction.channel
            self.clean_prefix = DEFAULT_PREFIX

    help_command.context = FakeContext(interaction)

    if command:
        cmd = self.bot.get_command(command)
        if cmd is None: 
            await help_command.command_not_found(command)
            return
        await help_command.send_command_help(cmd)
    else:
        mapping = help_command.get_bot_mapping()
        await help_command.send_bot_help(mapping)