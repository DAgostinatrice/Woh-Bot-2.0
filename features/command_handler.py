import re

import discord

from commands import set_presence, avatar, erp
from commands.admin import list_user_admin, add_user_admin, rm_user_admin
from commands.birthday import (set_channel_bd, show_channel_bd, set_user_bd, set_notif_time, list_user_bd,
                               manual_bd_check, show_message_bd, set_message_bd)
from commands.cant_be_disabled import disable, enable, help
from commands.music import play, leave, repeat, now_playing, resume, pause, volume, next, previous, queue, search


class CommandHandler(object):
    do_not_disable = ["enable", "disable", "help"]

    dict_cmd_name = "cmd_name"
    dict_enabled = "enabled"

    def __init__(self, client):
        self.parent_client = client

        self.commands = self.get_commands()
        self.set_every_command_state()

    def set_every_command_state(self):
        if self.parent_client.settings.user_command_states is None:
            return

        for cmd in self.commands:
            if self.command_state_exists(cmd.cmd_name):
                cmd.enabled = self.get_command_enabled(cmd.cmd_name)

    def get_command_enabled(self, cmd_name):
        if self.parent_client.settings.user_command_states is None:
            return None

        for cmd_state in self.parent_client.settings.user_command_states:
            if cmd_state[self.dict_cmd_name] == cmd_name:
                if cmd_state[self.dict_enabled] == "True":
                    return True
                else:
                    return False
        return None

    def command_state_exists(self, cmd_name):
        if self.parent_client.settings.user_command_states is None:
            return False

        for cmd_state in self.parent_client.settings.user_command_states:
            if cmd_state[self.dict_cmd_name] == cmd_name:
                return True
        return False

    def get_cmd(self, command_name):
        """Returns a Command with a command name

        :param command_name:
        :return: Command
        """
        for command in self.commands:
            if command.cmd_name == command_name:
                return command
        return None

    def get_commands(self):
        return [set_presence.SetPresence(self), disable.Disable(self), enable.Enable(self),
                manual_bd_check.ManualBDCheck(self), set_notif_time.SetNotifTime(self),
                add_user_admin.AddUserAdmin(self), rm_user_admin.RmUserAdmin(self),
                set_message_bd.SetMessageBD(self), show_message_bd.ShowMessageBD(self),
                set_channel_bd.SetChannelBD(self), show_channel_bd.ShowChannelBD(self),
                list_user_admin.ListUserAdmin(self), list_user_bd.ListUserBD(self), set_user_bd.SetUserBD(self),
                avatar.Avatar(self), play.Play(self), leave.Leave(self), resume.Resume(self), pause.Pause(self),
                now_playing.NowPlaying(self), repeat.Repeat(self), volume.Volume(self), previous.Previous(self),
                next.Next(self), queue.Queue(self), search.Search(self), erp.Erp(self), help.Help(self)]

    async def check_message(self, message: discord.Message):
        for cmd in self.commands:
            argument = re.compile("^" + self.parent_client.prefix + "[a-z]*").search(message.content.lower())
            if argument is not None:
                if argument.group() == self.parent_client.prefix + cmd.cmd_name:
                    await cmd.command(message)

    def get_cmd_inlines(self):
        return [cmd.get_help_inline() for cmd in self.commands]

    def enable_command(self, command_name):
        try:
            cmd = self.get_cmd(command_name)
            if cmd in self.do_not_disable:
                return "Attempted to enable an unchangeable command."
            cmd.enabled = True

            if self.command_state_exists(cmd.cmd_name):
                self.parent_client.settings.delete_command_state(
                    {self.dict_cmd_name: cmd.cmd_name, self.dict_enabled: "False"})
            return "Enabled '{}'!".format(command_name)
        except AttributeError:
            return "Failed to enable command, '{}' doesn't exist.".format(command_name)

    def disable_command(self, command_name):
        try:
            cmd = self.get_cmd(command_name)
            if cmd in self.do_not_disable:
                return "Attempted to disable an unchangeable command."
            cmd.enabled = False

            if not self.command_state_exists(cmd.cmd_name):
                self.parent_client.settings.save_user_defaults(
                    command_state={self.dict_cmd_name: cmd.cmd_name, self.dict_enabled: "False"})
            return "Disabled '{}'!".format(command_name)
        except AttributeError:
            return "Failed to disable command, '{}' doesn't exist.".format(command_name)
