import discord

import command_template


class Enable(command_template.Command):
    def __init__(self, handler):
        super(Enable, self).__init__(handler)

        self.enabled = True  # Should never change
        self.perm_level = self.permission_levels["owner"]
        self.cmd_name = "enable"
        self.arguments = "[command]"
        self.help_description = "Enables a command from the bot. This command can not be disabled."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        text_result = self.handler.enable_command(self.rm_cmd(message))
        await self.send_message_check(message.channel, text_result)
