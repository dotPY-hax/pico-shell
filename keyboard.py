import time
import usb_hid

from adafruit_hid.keyboard import Keyboard

import config


class KeyboardController:
    def __init__(self):
        self.keyboard = Keyboard(usb_hid.devices)
        self.layout = None
        self.change_layout(config.KEYBOARD_DEFAULT_LANG)

        self.back_channel = None

    def send_string(self, string):
        self.layout.write(string)

    def change_layout(self, layout_name):
        layout_name = f"keyboard_layout_win_{layout_name}"
        try:
            KeyboardLayout = __import__(f"layouts.{layout_name}", locals(), globals(), ["KeyboardLayout"]).KeyboardLayout
            self.layout = KeyboardLayout(self.keyboard)
        except ImportError:
            print(f"NO LAYOUT {layout_name}")

    def press_simultaneously(self, keycodes_to_press):
        for keycode in keycodes_to_press:
            self.keyboard.press(keycode)
            time.sleep(0.1)
        self.keyboard.release_all()
