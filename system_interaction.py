import time

from adafruit_hid.keycode import Keycode

import keyboard
from text_backchannel import BackChannel


class SystemInteraction:
    name = None

    def __init__(self):
        self.keyboard = keyboard.KeyboardController()

    def open_terminal(self):
        pass

    def command_with_back_channel(self):
        pass

    def close_terminal(self):
        self.keyboard.send_string("exit\n")

    def run_terminal_command(self, command, _exit=True):
        self.open_terminal()
        self.keyboard.send_string(command)
        self.keyboard.send_string("\n")
        if _exit:
            self.close_terminal()

    def establish_back_channel(self):
        back = BackChannel()
        if self.name == "linux":
            command = back.find_back_channel_mount_command()
        elif self.name == "windows":
            command = back.find_back_channel_powershell_command()
        else:
            command = ""

        self.run_terminal_command(command)
        time.sleep(5)
        back.check_for_back_channel_success()
        if back.back_channel_established:
            self.keyboard.back_channel = back

    def run_terminal_command_with_back_channel(self, command):
        if not self.keyboard.back_channel or not self.keyboard.back_channel.back_channel_established:
            self.establish_back_channel()
        if not self.keyboard.back_channel or not self.keyboard.back_channel.back_channel_established:
            return "NO BACK CHANNEL!! USE 'back': False"

        command = self.command_with_back_channel(command)
        self.run_terminal_command(command)
        time.sleep(1)
        result = self.keyboard.back_channel.read_back_channel()
        print(result)
        return result

class LinuxInteraction(SystemInteraction):
    name = "linux"

    def open_terminal(self):
        self.keyboard.press_simultaneously([Keycode.ALT, Keycode.CONTROL, Keycode.T])
        time.sleep(1)

    def command_with_back_channel(self, command):
        return self.keyboard.back_channel.command_with_back_channel_linux(command)

class WindowsInteraction(SystemInteraction):
    name = "windows"

    def open_terminal(self):
        self.keyboard.press_simultaneously([Keycode.WINDOWS, Keycode.R])
        time.sleep(0.5)
        self.keyboard.send_string("powershell.exe\n")
        time.sleep(1)
        self.keyboard.send_string("\n")

    def command_with_back_channel(self, command):
        return self.keyboard.back_channel.command_with_back_channel_windows(command)